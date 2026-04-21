from langchain_core.messages import HumanMessage, SystemMessage
from src.domain.ports.code_reviewer import CodeContent, ICodeReviewer, ReviewResult

# from langchain_ollama import ChatOllama
# from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

DEFAULT_REVIEW_RULES = [
    "El codigo debe seguir principios SOLID",
    "Las funciones deben tener una unica responsabilidad",
    "Los nombres de variables y funciones deben ser descriptivos",
    "El codigo debe incluir manejo de errores apropiados",
    "No debe haber codigo duplicado",
    "Las dependencias deben estar correctamente inyectadas",
    "El codigo debe ser testeable",
    "La documentacion debe ser clara y concisa",
]


class AICodeReviewer(ICodeReviewer):

    def __init__(self, api_key: str | None = None, model: str = "gemini-2.5-flash"):
        self._api_key = api_key
        self._model = model
        self._rules = DEFAULT_REVIEW_RULES

    def review_code(self, code: CodeContent) -> ReviewResult:

        sysyem_prompt = self._build_system_prompt()
        user_prompt = self._build_review_prompt(code)

        llm = ChatGoogleGenerativeAI(model=self._model, api_key=self._api_key)

        response = llm.invoke(
            [
                SystemMessage(content=sysyem_prompt),
                HumanMessage(content=user_prompt),
            ]
        )
        print(f"RESPONSE CONTENT FOM LLM{response.content}")
        print(f"RESPONSE  FOM LLM{response}")

        return self._parse_response(response.content)

    def _build_system_prompt(self) -> str:
        rules_text = "\n".join(f" - {rule}" for rule in self._rules)

        return (
            "Sos un revisor de codigo experto. Evalua el codigo basado en estas reglas:\n"
            f"{rules_text}\n\n"
            "Responde en este formato exacto:\n"
            "RATING:<numner 0 a 100>\n"
            "SUMMARY:<un parrafo de summary>\n"
            "RECOMMENDATIONS:\n"
            "- <recommendation 1>\n"
            "- <recommendation 2>\n"
            "- <recommendation 3>\n"
            "..."
        )

    def _build_review_prompt(self, code: CodeContent) -> str:
        files_text = ""

        for filepath, content in code.files.items():
            files_text += f"\n-- {filepath} --\n{content}\n"

        return (
            f"PR: Title: {code.pr_title}\n"
            f"PR: Description: {code.pr_description}\n"
            f"Folder Structure: {', '.join(code.folder_structure)}/n"
            f"\nFiles:\n{files_text}"
        )

    def _parse_response(self, content: str) -> ReviewResult:

        lines = content.strip().split("\n")
        rating = 50
        summary = ""
        recommendations = []

        for i, line in enumerate(lines):
            if line.startswith("RATING:"):
                try:
                    rating = int(line.split(":")[1].strip())
                except (ValueError, IndexError):
                    rating = 50

            elif line.startswith("SUMMARY:"):
                summary = line.split(":", 1)[1].strip()
            elif (
                line.startswith("- ")
                and i > 0
                and any(
                    lines[j].startswith("RECOMMENDATIONS")
                    for j in range(max(0, i - 5), i)
                )
            ):
                recommendations.append(line[2:].strip())

        return ReviewResult(
            rating=max(0, min(100, rating)),
            summary=summary,
            recommendations=recommendations,
        )

    def get_review_rules() -> list[str]:
        pass
