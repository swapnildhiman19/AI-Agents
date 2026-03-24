# from google.adk.agents.llm_agent import Agent

# root_agent = Agent(
#     model='<FILL_IN_MODEL>',
#     name='root_agent',
#     description='A helpful assistant for user questions.',
#     instruction='Answer user questions to the best of your knowledge',
# )

from google.adk.agents.llm_agent import Agent

# Mock Tool Implementation
def get_current_time(city: str) -> dict:
    """Returns the current time in specified city."""
    return {"status":"success", "city":city, "time":"10:30 PM"}

root_agent = Agent(
    model = 'gemini-3-flash-preview',
    name = 'root_agent',
    description = 'Tells the current time in a specified city.',
    instruction = 'You are a helpful assistant that tells the current time in a specified city. Use the get_current_time tool to get the current time in a specified city.',
    tools = [get_current_time],
)