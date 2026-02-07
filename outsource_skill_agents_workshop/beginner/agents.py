import os

from crewai import Agent
from crewai.llm import LLM
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model="openai/gpt-4o",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0.7,
    max_tokens=4000,
    timeout=120
)

hate_speech_detector = Agent(
    role="Hate Speech Detector",
    goal="Analyse the text and identify if any hate speech or offensive language is present",
    llm=llm,
    backstory=(
        "You are a Hate Speech Detector who understands details very well and is an expert at identifying hate speech or offensive language in given text."
    )
)