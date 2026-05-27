from src.domain.ports.code_reviewer import ICodeReviewer, CodeContent, ReviewResult
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

DEFAULT_REVIEW_RULES = [
    'El codigo debe seguir los principios SOLID',
    'Las funciones deben tener una unica responsabilidad',
    'Los nombres de variables y funciones deben ser descriptivos',
    'No debe de haber codigo duplicado',
    'Las dependencias deben estar correctamente inyectadas',
    'El codigo debe ser testeable',
    'La documentacion debe ser clara y concisa'
]


class AICodeReviewer(ICodeReviewer):
    
    
    def __init__(self, api_key: str, model:str='gpt-4o'):
        self._api_key = api_key
        self._model = model
        self._rules = DEFAULT_REVIEW_RULES

    
    def review_code(self, code: CodeContent) -> ReviewResult:
        
        llm = ChatOpenAI(
            model=self._model,
            api_key=self._api_key
        )
        
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_review_prompt(code)
        
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
            
        ])
        
        return self._parse_response(response.content)
        
    def _build_system_prompt(self)-> str:
        rules_text = "\n".join(f" - {rule}" for rule in self._rules)
        return (
            "Eres un revisor de codigo experto, evalua el codigo basado en estas reglas:\n"
            f"{rules_text}\n\n"
            "Responde en este formato exacto:\n"
            "RATING: <number 0-100>\n"
            "SUMMARY: <un parrafo de summary>\n"
            "RECOMMENDATIONS:\n"
            "- <recomendation 1>\n"
            "- <recomendation 2>\n"
        )
        
        
    def get_review_rules(self) -> list[str]:
        return self._rules.copy()
        
        
        
    def _build_review_prompt(self, code: CodeContent) -> str:
        files_text = ""
        for filepath, content in code.files.items():
            files_text += f"\n---{filepath}---\n{content}\n"
        
        return (
            f"PR Title: {code.pr_title}\n"
            f"PR Description: {code.pr_description}\n"
            f"Folder Structure: {', '.join(code.folder_structure)}\n"
            f"\nFiles:\n {files_text}\n"
        )
        
    def _parse_response(self,content: str) -> ReviewResult:
        lines = content.strip().split("\n")
        rating = 50
        summary = ""
        recommendations = []
        
        for i, line in enumerate(lines):
            if line.startswith("RATING:"):
                try:
                    rating= int(line.split(":")[1].strip())
                except(ValueError,IndexError):
                    rating = 50
            elif line.startswith('SUMMARY:'):
                summary = line.split(":",1)[1].strip()
            elif line.startswith('- ') and i > 0 and any(
                lines[j].startswith("RECOMMENDATIONS:") for j in range(max(0,i - 5),i)
            ):
                
                recommendations.append(line[2:].strip())
                
        return ReviewResult(
                rating=max(0,min(100,rating)),
                summary=summary,
                recommendations=recommendations
            )   
    
     
        