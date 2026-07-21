# app/agents/root_agent.py
from google.adk.agents import SequentialAgent
from app.agents.classifier_agent import classifier_agent
from app.agents.extractor_agent import extractor_agent
from app.agents.validator_agent import validator_agent

root_agent = SequentialAgent(
    name="document_extraction_pipeline",
    description="Classifies, extracts, and validates data from an uploaded document.",
    sub_agents=[classifier_agent, extractor_agent, validator_agent],
)