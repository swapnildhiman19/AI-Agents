from google.adk.agents.llm_agent import LlmAgent
from pydantic import BaseModel, Field

# Pydantic is being used to define the structure of the output of the agent.
class CapitalOutput(BaseModel):
    capital : str = Field(description='The capital of the country')

# root_agent = LlmAgent(
#     model='gemini-2.5-flash',
#     name='root_agent',
#     description='A helpful assistant for user questions.',
#     instruction='Answer user questions to the best of your knowledge',
# )

# adk web expects it to have atleast one root_agent.
root_agent = LlmAgent(
    name='capital_agent',
    model='gemini-3-flash-preview',
    description='A helpful assistant for telling the capital of a country',
    instruction="""
    You are a Capital Information Agent. Given country, respond ONLY with a JSON object containing the capital.
    Example:
    Input: "What is the capital of France?"
    Output: {"capital": "Paris"}
    If the country is not found, return JSON object with "capital" key set to "Unknown country".
    Example:
    Input: "What is the capital of Random1234 country?"
    Output: {"capital": "Unknown country"}
    """,
    output_schema=CapitalOutput,
    output_key='capital'
)