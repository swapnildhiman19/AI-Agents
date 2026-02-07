from crewai import Task


def get_hate_speech_detection_task(agent):
    return Task(
        description="Find if there is any hate speech or offensive language in the text.\nText: {text}",
        expected_output="Respond with 'hate speech' or 'no hate speech'",
        agent=agent
    )