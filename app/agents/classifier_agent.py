# app/agents/classifier_agent.py
from google.adk.agents import LlmAgent
from app.schema import DocumentClassification
from app.environment import GEMINI_MODEL

classifier_agent = LlmAgent(
    name="classifier_agent",
    model=GEMINI_MODEL,
    description="Classifies the type of an uploaded document.",
    instruction="""
You are a document classification specialist.
You will receive a document (image or PDF) as an attached artifact.
Look at it and determine what type of document it is
(invoice, receipt, id_card, contract, resume, form, other).
Return only the classification.
""",
    output_schema=DocumentClassification,
    output_key="classification",   # written to session.state["classification"]
)