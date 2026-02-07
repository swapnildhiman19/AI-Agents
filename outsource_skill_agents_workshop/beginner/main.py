from crewai import Crew
from agents import hate_speech_detector
from tasks import get_hate_speech_detection_task

hate_speech_detection_task = get_hate_speech_detection_task(hate_speech_detector)

crew = Crew(
    agents=[hate_speech_detector],
    tasks=[hate_speech_detection_task],
    memory=False,
    verbose=True
)

text = " Public libraries are great for learning and research."
result = crew.kickoff(input=text)
print(result)