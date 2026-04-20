from domain.ports.code_reviewer import CodeContent

from pathlib import Path

from infrastructure.ai.ai_code_reviewer import AICodeReviewer


reviewer = AICodeReviewer()

simple_file = Path(__file__).parent / "code_example.py"

code = CodeContent(
    files={"src/utils.py": simple_file.read_text()},
    folder_structure=["src"],
    pr_title="Probando un utils",
    pr_description="New utiliy to filter and transform",
)

print("MANANDO A REVISAR CODIGO")
result = reviewer.review_code(code)


print("RESULTADO CRUDO")
print(result)


print(f"RATING:{result.rating}")
print(f"SUMMARY:{result.summary}")
print(f"RECOMMENDATIONS:{result.recommendations}")
