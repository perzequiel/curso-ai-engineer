from dotnev import load_dotenv

load_dotenv()

from infrastructure.ai.old_langgraph_code_reviewer import LangGraphCodeReviewer

sample_file = Path(__file__).parent / "sample_code.py"

input_state = {
    "files": {"src/utils.py": sample_file.read_text()},
    "folder_structure": ["src"],
    "pr_title": "Add data processing utility",
    "pr_description": "New utility function to filter and transform positive reviews for better insights.",
}

print("Executing Graph...")
result = graph.invoke(input_state)

print(f"\n{'='*50}")
print(f"Rating: {result['rating']}/100")
print(f"Approved: {result['approved']}")
print(f"Summary: {result['summary']}")
print(f"Recommendations:")
for rec in result["recommendations"]:
    print(f"  - {rec}")

if result["study_plan"]:
    print(f"\n{'='*50}")
    print("Study Plan:")
    print(result["study_plan"])