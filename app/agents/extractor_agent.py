# app/agents/extractor_agent.py
from google.adk.agents import LlmAgent
from app.schema import ExtractionResult
from app.environment import GEMINI_MODEL

extractor_agent = LlmAgent(
    name="extractor_agent",
    model=GEMINI_MODEL,
    description="Extracts structured fields from the document.",
    instruction="""
You are a document data extraction specialist.
The document type was classified as: {classification}

Look at the attached document artifact and extract every relevant field
(e.g. names, dates, amounts, IDs, addresses) as field_name/value pairs.
Be exhaustive but do not invent values that are not present in the document.
""",
    output_schema=ExtractionResult,
    output_key="extraction",
)