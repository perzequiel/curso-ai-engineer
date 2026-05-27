"""Test standalone del AICodeReviewer con la API real de Anthropic."""

import os
from pathlib import Path
from dotenv import load_dotenv
from src.domain.ports.code_reviewer import CodeContent
from src.infrastructure.ai.ai_code_reviewer import AICodeReviewer
# from src.infrastructure.ai.op_code_reviewer import OPCodeReviewer
from src.infrastructure.ai.langgraph_code_reviewer import LangGraphCodeReviewer

load_dotenv()

key_path = "OPENAI_API_KEY"
# key_path = "GOOGLE_API_KEY"
# api_key = os.environ.get("ANTHROPIC_API_KEY")
api_key = os.environ.get(key_path)
if not api_key:
    raise RuntimeError(f"{key_path} no esta configurada en .env")

reviewer = AICodeReviewer(api_key=api_key)
# reviewer = OPCodeReviewer(api_key=api_key)
#reviewer = LangGraphCodeReviewer(api_key=api_key)

sample_file = Path(__file__).parent / "sample_code.py"
code = CodeContent(
    files={"src/utils.py": sample_file.read_text()},
    folder_structure=["src"],
    pr_title="Add data processing utility",
    pr_description="New utility function to filter and transform positive numbers",
)

print("Enviando codigo a revisar...")
result = reviewer.review_code(code)

print(f"\nRating: {result.rating}")
print(f"Summary: {result.summary}")
print(f"Recommendations:")
for rec in result.recommendations:
    print(f"  - {rec}")
