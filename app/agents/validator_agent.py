# app/agents/validator_agent.py
from google.adk.agents import LlmAgent
from app.schema import ValidatedResult
from app.environment import GEMINI_MODEL

validator_agent = LlmAgent(
    name="validator_agent",
    model=GEMINI_MODEL,
    description="Validates and cleans the extracted JSON.",
    instruction="""
Review this extraction result: {extraction}

Check for: missing required fields for a document of this type, malformed
dates/amounts, or obviously inconsistent values. Fix minor formatting issues
yourself (e.g. date normalization). Flag anything you couldn't confidently fix
in `issues`. Set is_valid to false only if there's a serious problem.
""",
    output_schema=ValidatedResult,
    output_key="final_result",
)