from src.domain.ports.code_reviewer import ICodeReviewer, CodeContent, ReviewResult

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

DEFAULT_REVIEW_RULES = [
    "The code must follow SOLID principles",
    "Functions must have a single responsibility",
    "Variable and function names must be descriptive",
    "The code must include appropriate error handling",
    "There must be no duplicated code",
    "Dependencies must be correctly injected",
    "The code must be testable",
    "Documentation must be clear and concise",
]

"""Adapter of the port AICodeReviewer, this class is the one that is going to be used in the application layer, it will receive the code and send it to the LLM, then it will parse the response and return a ReviewResult."""
class AICodeReviewer(ICodeReviewer):

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5-20250929", rules: str = ""):
            self._api_key = api_key
            self._model = model
            self._rules = rules

    """ Receive the code, part makes the LLM work"""
    def review_code(self, code: CodeContent) -> ReviewResult:
         
        """ I instantiate ChatAntropic wrapper sendint the configuration of the model claude-sonnet in this case and its API_key"""
        llm = ChatAnthropic(
             model=self._model,
             api_key=self._api_key,
        )

        system_prompt = self._build_system_prompt()
        """I built the user prompt which is the action that is going to wait regarding the prompt that I have created _build_system_prompt"""
        user_prompt = self._build_review_prompt(code)
        """This is the _build_review_prompt response"""
        response = llm.invoke([
             SystemMessage(content=system_prompt),
             HumanMessage(content=user_prompt),
        ])
        """I should return a ReviewResult, for that I should take the LLM response, parse it. See where it returned the rating, the summary and the recommendations. For that I need to parse the ReviewResult."""
        return self._parse_response(response.content)
    
    def get_review_rules(self) -> list[str]:
        return "\n".join(self._rules)

    """I create a SystemPrompt that will give the role configuration of the user which is how the answer is going to be."""
    def _build_system_prompt(self) -> str:
        rules_text = "\n".join("" for rule in self._rules)
        return (
                "You are an expert code reviewer. Evaluate the code based on these rules:\n"
                f"{rules_text}\n\n"
                "Respond in this exact format:\n"
                "RATING: <number 0-100>\n"
                "SUMMARY: <one paragraph summary>\n"
                "RECOMMENDATIONS:\n"
                "- <recommendation 1>\n"
                "- <recommendation 2>\n"
                "..."
            )
    """Here it is being send a parsed code, converting it into text in order to send it to the LLM"""
    def _build_review_prompt(self, code: CodeContent) -> str:
        files_text = ""
        for filepath, content in code.files.items():
            files_text += f"\n--- {filepath} ---\n{content}\n"

        return (
             f"PR Title: {code.pr_title}\n"
             f"PR Description: {code.pr_description}\n"
             f"Folder Structure: {', '.join(code.folder_structure)}\n"
             f"Files:\n{files_text}"
        )
    
    def _parse_response(self, content: str) -> ReviewResult:
        """The content is the LLM response """
        lines = content.strip().split("\n")
        rating = 50
        summary = ""
        recommendations = []
        
        for i, line in enumerate(lines):
            if line.startswith("RATING:"):
                try:
                    rating = int(line.split("RATING:")[1].strip())
                except (ValueError, IndexError):
                   rating = 50
            elif line.startswith("SUMMARY:"):
                summary = line.split(":", 1)[1].strip()
            elif line.startswith("-") and any(
                lines[j].startswith("RECOMMENDATIONS") for j in range(max(0, i -5), i)):
                recommendations.append(line[2:].strip())
        
        return ReviewResult(
            rating=max(0, min(100, rating)),
            summary=summary, 
            recommendations=recommendations
        )
    