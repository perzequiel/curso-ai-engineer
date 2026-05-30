from src.domain.ports.code_reviewer import ICodeReviewer, CodeContent, ReviewResult

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

DEFAULT_REVIEW_RULES = [
    "The code must follow SOLID principles",
    "Functions must have a single responsibility",
    "Variable and function names must be descriptive",
    "The code must include appropriate error handling",
    "There must be no duplicated code",
    "Dependencies must be correctly injected",
    "The code must be testable",
    "Documentation must be clear and concise"
]

class OPCodeReviewer(ICodeReviewer):

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
            self._api_key = api_key
            self._model = model
            self._rules = DEFAULT_REVIEW_RULES

    """ReviewResult is my domain object. In Domain, my DTO. I need to parse the LLM response and convert it into a ReviewResult object that I can return."""
    def review_code(self, code: CodeContent) -> ReviewResult:
         
        llm = ChatGoogleGenerativeAI(
             model=self._model,
             google_api_key=self._api_key,
        )

        system_prompt = self._build_system_prompt()
        user_prompt = self._build_review_prompt(code)

        response = llm.invoke([
             SystemMessage(content=system_prompt),
             HumanMessage(content=user_prompt),
        ])
        return self._parse_response(response.content)
    
    def get_review_rules(self) -> list[str]:
        return self._rules.copy()

    def _build_system_prompt(self) -> str:
        rules_text = "\n".join(f"- {rule}" for rule in self._rules)
        return (
                "You are an expert code reviewer. Evaluate the code based on these rules:\n"
                f"{rules_text}\n\n"
                "Respond in this exact format:\n"
                "RATING: <number 0-100>\n"
                "SUMMARY: <one-paragraph summary>\n"
                "RECOMMENDATIONS:\n"
                "- <recommendation 1>\n"
                "- <recommendation 2>\n"
                "..."
        )
    
    def _build_review_prompt(self, code: CodeContent) -> str:
        files_text = ""
        for filepath, content in code.files.items():
            files_text += f"\n--- {filepath} ---\n{content}\n"

        return (
             f"PR Title: {code.pr_title}\n"
             f"PR Description: {code.pr_description}\n"
             f"Folder Structure: {', '.join(code.folder_structure)}\n"
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
             elif line.startswith("- ") and i > 0 and any(
                 lines[j].startswith("RECOMMENDATIONS") for j in range(max(0, i -5), i)
            ):
                recommendations.append(line[2:].strip())
        
         return ReviewResult(
            rating=int(max(0, min(100, rating))),
            summary=str(summary), 
            recommendations=list(recommendations) 
        )
