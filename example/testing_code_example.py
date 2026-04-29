from pathlib import Path
import os

from dotenv import load_dotenv

from domain.ports.code_reviewer import CodeContent

from infrastructure.ai.ai_code_reviewer import AICodeReviewer
from infrastructure.ai.langraph_code_reviewer import LangraphCodeReviewer

load_dotenv()

# reviewer = AICodeReviewer(
#     api_key=os.getenv("GOOGLE_API_KEY"),
#     model="gemini-2.5-flash",
# )
reviewer = LangraphCodeReviewer(api_key=os.getenv("GOOGLE_API_KEY"))
simple_file = Path(__file__).parent / "code_example.py"

code = CodeContent(
    files={"src/utils.py": simple_file.read_text()},
    folder_structure=["src"],
    pr_title="Probando un utils",
    pr_description="New utiliy to filter and transform",
)

print("MANDANDO A REVISAR CODIGO")
result = reviewer.review_code(code)


print("RESULTADO CRUDO")
print(result)


print(f"RATING:{result.rating}")
print(f"SUMMARY:{result.summary}")
print(f"RECOMMENDATIONS:{result.recommendations}")
