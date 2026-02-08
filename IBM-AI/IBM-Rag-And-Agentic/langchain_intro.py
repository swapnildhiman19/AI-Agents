from dotenv import parser
from langchain_core.prompts import PromptTemplate
prompt_template = PromptTemplate.from_template(
    "Tell me a {adjective} joke about {content}"
)

prompt = prompt_template.format(adjective="funny", content="cats")
print(prompt)
