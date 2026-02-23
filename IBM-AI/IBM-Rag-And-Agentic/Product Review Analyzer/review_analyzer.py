"""
Review Analyzer: terminal app that analyzes a product review,
classifies sentiment, extracts key points, and writes a customer response.
Uses Google Gemini via LangChain (LCEL).
"""

import os
from dotenv import load_dotenv

# Remove proxy if needed (e.g. corporate VPN)
for proxy_var in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"]:
    os.environ.pop(proxy_var, None)

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Set GOOGLE_API_KEY in your .env file")

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# ----- LLM -----
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY,
    max_output_tokens=1024,
    temperature=0.3,
)

# ----- Prompt templates -----
sentiment_template = """Analyze the sentiment of the following product review as positive, negative, or neutral.
Provide your analysis in the format: "SENTIMENT: [positive/negative/neutral]"

Review: {review}

Your analysis:
"""

summary_template = """Summarize the following product review into 3-5 key bullet points.
Each bullet point should be concise and capture an important aspect mentioned in the review.

Review: {review}
Sentiment: {sentiment}

Key points:
"""

response_template = """Write a helpful response to a customer based on their product review.
If the sentiment is positive, thank them for their feedback. If negative, express understanding
and suggest a solution or next steps. Personalize based on the specific points they mentioned.

Review: {review}
Sentiment: {sentiment}
Key points: {summary}

Response to customer:
"""

# ----- Prompts and chains -----
sentiment_prompt = PromptTemplate.from_template(sentiment_template)
summary_prompt = PromptTemplate.from_template(summary_template)
response_prompt = PromptTemplate.from_template(response_template)

sentiment_chain = sentiment_prompt | llm | StrOutputParser()
summary_chain = summary_prompt | llm | StrOutputParser()
response_chain = response_prompt | llm | StrOutputParser()

# ----- Full LCEL pipeline (same as notebook) -----
review_chain = (
    RunnablePassthrough.assign(
        sentiment=lambda x: sentiment_chain.invoke({"review": x["review"]})
    )
    | RunnablePassthrough.assign(
        summary=lambda x: summary_chain.invoke({
            "review": x["review"],
            "sentiment": x["sentiment"],
        })
    )
    | RunnablePassthrough.assign(
        response=lambda x: response_chain.invoke({
            "review": x["review"],
            "sentiment": x["sentiment"],
            "summary": x["summary"],
        })
    )
)


def analyze(review_text):
    """Run the full pipeline and return sentiment, summary, response."""
    return review_chain.invoke({"review": review_text})


def main():
    print("=" * 60)
    print("  REVIEW ANALYZER (Google Gemini)")
    print("  Enter a product review; get sentiment, key points, and a customer response.")
    print("  Type 'quit' or 'exit' to stop.")
    print("=" * 60)

    while True:
        print()
        review = input("Paste your review (or 'quit'): ").strip()
        if review.lower() in ("quit", "exit", "q"):
            print("Bye.")
            break
        if not review:
            print("No input. Try again or type 'quit'.")
            continue

        print("\nAnalyzing...")
        try:
            out = analyze(review)
            print("\n--- SENTIMENT ---")
            print(out["sentiment"])
            print("\n--- KEY POINTS ---")
            print(out["summary"])
            print("\n--- RESPONSE TO CUSTOMER ---")
            print(out["response"])
        except Exception as e:
            print(f"Error: {e}")
        print()


if __name__ == "__main__":
    main()