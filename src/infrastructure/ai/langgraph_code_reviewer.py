from src.domain.ports.code_reviewer import ICodeReviewer, CodeContent, ReviewResult

from typing import Annotated, TypedDict

# from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

DEFAULT_REVIEW_RULES = [
    "El codigo debe seguir principios SOLID",
    "Las funciones deben tener una unica responsabilidad",
    "Los nombres de variables y funciones deben ser descriptivos",
    "El codigo debe incluir manejo de errores apropiado",
    "No debe haber codigo duplicado",
    "Las dependencias deben estar correctamente inyectadas",
    "El codigo debe ser testeable",
    "La documentacion debe ser clara y concisa",
]

RATING_THRESHOLD = 99

class ReviewState(TypedDict):
    # inputs
    files: dict[str, str]
    folder_structure: list[str]
    pr_title: str
    pr_description: str
    # review output
    rating: int
    summary: str
    recommendations: list[str]
    # validation output
    approved: bool
    study_plan: str

class LangGraphCodeReviewer(ICodeReviewer):

    # def __init__(self, api_key: str, model: str = "claude-sonnet-4-5-20250929"):
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        self._api_key = api_key
        self._model = model
        self._rules = DEFAULT_REVIEW_RULES

    def review_code(self, code: CodeContent) -> ReviewResult:
        graph = self._build_graph()
        result = graph.invoke({
            "files": code.files,
            "folder_structure": code.folder_structure,
            "pr_title": code.pr_title,
            "pr_description": code.pr_description,
        })

        return ReviewResult(
            rating=result["rating"],
            summary=result["study_plan"],
            recommendations=result["recommendations"],
        )


    def get_review_rules(self) -> list[str]:
        return self._rules.copy()
    
    def _call_llm(self, system_prompt, user_prompt) -> str:
        
        # llm = ChatAnthropic(
        llm = ChatGoogleGenerativeAI(    
            model=self._model,
            api_key=self._api_key
        )

        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])

        return response.content

    # nodes
    # _review_node
    def _review_node(self, state: ReviewState) -> dict:
        """Revisa el codigo y genera rating + summary + recommendations."""

        rules_text = "\n".join(f" - {r}" for r in self._rules)
        system = (
            "Sos un revisor de codigo experto. Evalua el codigo basado en estas reglas:\n"
            f"{rules_text}\n\n"
            "Responde en este formato exacto:\n"
            "RATING: <number 0-100>\n"
            "SUMMARY: <un parrafo>\n"
            "RECOMMENDATIONS:\n"
            "- <recommendation 1>\n"
            "- <recommendation 2>\n"
            "..."
        )

        files_text = ""
        for fp, content in state["files"].items():
            files_text += f"\n--- {fp} ---\n{content}\n"

        user = (
            f"PR Title: {state['pr_title']}\n"
            f"PR Description: {state['pr_description']}\n"
            f"Folder Structure: {', '.join(state['folder_structure'])}\n"
            f"\nFiles:\n{files_text}"
        )

        content = self._call_llm(system, user)
        return self._parse_review(content)
    
    # _validate_rating_node
    def _validate_rating_node(self, state: ReviewState) -> dict:
        """Si el rating es bajo, genera un plan de estudio con conceptos a mejorar."""
        rating = state["rating"]
        summary = state['summary']
        recommendations = state["recommendations"]

        if rating >= RATING_THRESHOLD:
            return {"approved": True, "study_plan": ""}

        system = (
            "Sos un mentor de programacion. Dado un code review con rating bajo, "
            "genera un plan de estudio conciso con los conceptos que el desarrollador "
            "necesita estudiar para mejorar su codigo.\n\n"
            "Formato:\n"
            "PLAN DE ESTUDIO:\n"
            "1. <Concepto> — <por que es importante y recurso sugerido>\n"
            "2. ...\n"
        )

        user = (
            f"Rating: {rating}/100 (threshold: {RATING_THRESHOLD})\n"
            f"Summary: {summary}\n"
            f"Recommendations:\n"
            + "\n".join(f"- {r}" for r in recommendations)
        )

        content = self._call_llm(system, user)

        return {"approved": False, "study_plan": content}

    # parse review
    def _parse_review(self, content: str) -> dict:
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
                lines[j].startswith("RECOMMENDATIONS") for j in range(max(0, i - 5), i)
            ):
                recommendations.append(line[2:].strip())

        return {
            "rating": max(0, min(100, rating)),
            "summary": summary,
            "recommendations": recommendations,
        }
    
    def _build_graph(self) -> StateGraph:
        graph = StateGraph(ReviewState)

        graph.add_node("review", self._review_node)
        graph.add_node("validate_rating", self._validate_rating_node)

        graph.set_entry_point("review")
        graph.add_edge("review", "validate_rating")
        graph.add_edge("validate_rating", END)

        return graph.compile()


