"""Entry point for LangGraph Studio. Does not affect production code."""
import os
from dotenv import load_dotenv
from src.infrastructure.ai.langgraph_code_reviewer import LangGraphCodeReviewer

load_dotenv()

api_key = os.environ.get("ANTHROPIC_API_KEY", "")
graph = LangGraphCodeReviewer(api_key=api_key)._build_graph()
