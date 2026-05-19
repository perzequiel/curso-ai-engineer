from src.domain.ports.code_reviewer import ICodeReviewer, ReviewResult, CodeContent  
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
import json
import re

DEFAULT_REVIEW_RULES = [
    "La documentación debe ser clara, concisa y estar actualizada.",
    "El código debe ser fácilmente testeable y contar con pruebas automatizadas.",
    "Las dependencias deben estar correctamente inyectadas y gestionadas.",
    "El código debe seguir los principios SOLID.",
    "Cada función debe tener una única responsabilidad.",
    "Los nombres de variables, funciones y clases deben ser descriptivos y consistentes.",
    "El código debe incluir manejo de errores apropiado y mensajes claros.",
    "Evitar duplicación de código (DRY).",
    "El código debe ser legible y mantener un estilo consistente (PEP8 u otro estándar).",
    "Los comentarios deben aportar valor y no explicar lo obvio.",
    "No debe haber código muerto, sin usar o comentado innecesariamente.",
    "Las entradas y salidas de funciones deben estar validadas.",
    "El código debe ser eficiente y evitar complejidad innecesaria.",
    "Las configuraciones sensibles (API keys, passwords) no deben estar hardcodeadas.",
    "El código debe ser modular y fácil de mantener.",
    "Las dependencias externas deben estar documentadas y justificadas.",
    "Las estructuras de datos deben ser apropiadas para el problema.",
    "El código debe ser seguro y proteger contra vulnerabilidades comunes.",
    "Las migraciones o cambios en base de datos deben estar versionados.",
    "El código debe ser compatible con el entorno y versiones especificadas.",
]

class AICodeReviewer(ICodeReviewer):
    def __init__(self, api_key: str, model: str="gemini-2.5-flash"):
        self._api_key=api_key #Dejamos privado el seteo del valor con '_' 
        self._model= model  #Como no vamos a modificar el modelo, lo dejamos privado para encapsular la información
        self._rules=DEFAULT_REVIEW_RULES

    def review_code(self, code: CodeContent) -> ReviewResult:
        llm=ChatGoogleGenerativeAI(
            model=self._model,
            google_api_key=self._api_key
        )
        system_prompt=self._build_system_prompt() #Sirve para definir el “rol”, el tono, las reglas o el contexto general que debe seguir el modelo durante toda la conversación.
        user_prompt=self._build_review_prompt(code)
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])
        return self._parse_response(response.content)
    
    def _build_system_prompt(self) -> str:
        rules_text="\n".join (f"- {rule}" for rule in self._rules)
        return f"""
        Sos un senior software engineer con más de 10 años de experiencia en code review.
        Tu objetivo es evaluar Pull Requests de forma objetiva, constructiva y accionable.

        ## REGLAS DE EVALUACIÓN
        Usá exclusivamente las siguientes reglas para calificar el código:
        <rules>
        {rules_text}
        </rules>

        ## INSTRUCCIONES
        - Analizá CADA archivo del PR antes de responder.
        - Sé directo: no suavices problemas críticos.
        - Las recomendaciones deben ser accionables y específicas (no genéricas).
        - El rating debe reflejar fielmente el cumplimiento de las reglas provistas.

        ## FORMATO DE RESPUESTA
        Respondé ÚNICAMENTE con un JSON válido con la siguiente estructura.
        Responde SIEMPRE en Español NEUTRO.
        Sin markdown, sin bloques ```json, sin texto antes o después.

        {{
        "rating": <entero entre 0 y 100>,
        "summary": "<un párrafo con el diagnóstico general del PR>",
        "recommendations": [
            {{
            "severity": "<critical|major|minor|suggestion>",
            "description": "<qué está mal o qué mejorar>",
            "suggestion": "<cómo corregirlo"
            }}
        ]
        }}""".strip()
    
    def _build_review_prompt(self, code: CodeContent)-> str:
        """
        Construye el prompt de usuario para enviar al modelo, con el contenido del PR.
        """
        #Archivos con su contenido
        files_text = ""
        for filepath, content in code.files.items():
            files_text += f"\n### {filepath}\n```\n{content}\n```\n"
        #Estrcutura de carpetas como arbol
        folder_structure= "\n" .join (f" - {folder}" for folder in code.folder_structure)
        return (
        f"## Pull Request a revisar\n\n"
        f"**Título:** {code.pr_title}\n\n"
        f"**Descripción:**\n{code.pr_description or 'Sin descripción.'}\n\n"
        f"**Estructura de carpetas:**\n{folder_structure}\n\n"
        f"**Archivos modificados:**\n{files_text}\n"
    )
    
    def _parse_response(self, content: str) -> ReviewResult:
        """
        Parsea el string JSON que devuelve el LLM y lo convierte en ReviewResult.
        """
        data = None

        # Intento 1: JSON puro
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            pass

        # Intento 2: El LLM mandó ```json ... ``` igual
        if data is None:
            match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", content)
            if match:
                try:
                    data = json.loads(match.group(1))
                except json.JSONDecodeError:
                    pass

        # Intento 3: Buscar el primer { ... } que encuentre
        if data is None:
            match = re.search(r"\{[\s\S]*\}", content)
            if match:
                try:
                    data = json.loads(match.group())
                except json.JSONDecodeError:
                    pass

        # Si ninguno funcionó, devolver ReviewResult de error
        if data is None:
            return ReviewResult(
                rating=-1,
                summary=f"Error al parsear la respuesta del modelo: {content[:200]}",
                recommendations=[],
            )

        # ── Normalizar rating ─────────────────────────────────────────────────
        try:
            rating = int(data.get("rating", -1))
            if not (0 <= rating <= 100):
                rating = -1
        except (ValueError, TypeError):
            rating = -1

        # ── Normalizar summary ────────────────────────────────────────────────
        summary = data.get("summary") or "Sin resumen."

        # ── Normalizar recommendations → siempre list[str] ───────────────────
        # El LLM puede mandar objetos {severity, description, suggestion} -> entonces aplanamos para que coincida con List[]
        raw_recs = data.get("recommendations", [])
        recommendations = []
        for rec in raw_recs:
            if isinstance(rec, str):
                recommendations.append(rec)
            elif isinstance(rec, dict):
                parts = filter(None, [
                    f"[{rec.get('severity', '').upper()}]" if rec.get("severity") else None,
                    rec.get("description", ""),
                    f"→ {rec.get('suggestion')}" if rec.get("suggestion") else None,
                ])
                recommendations.append(" ".join(parts))

        return ReviewResult(
            rating=rating,
            summary=summary,
            recommendations=recommendations,
        )
    
    def get_review_rules(self) -> list[str]:
        return self._rules   
    