import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# ============================================================
# Remove proxy settings (for Walmart VPN)
# ============================================================
for proxy_var in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"]:
    os.environ.pop(proxy_var, None)

# ============================================================
# Load API key
# ============================================================
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Please set your GOOGLE_API_KEY in the .env file!")

# ============================================================
# Initialize the LangChain Chat Model
# ============================================================
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY,
    max_output_tokens=512,
    temperature=0.4,
)

# ============================================================
# Conversation history + chat functions
# ============================================================
SYSTEM_PROMPT = "You are a helpful assistant who plays a role of iOS interviewer who is hiring for iOS Developer in Indian Startup which is at par with on going trends of AI."

conversationHistory = [
    SystemMessage(content=SYSTEM_PROMPT)
]

def chat_with_llm(user_input):
    """Send user message to LLM, store in history, return AI response text."""
    conversationHistory.append(HumanMessage(content=user_input))
    response = llm.invoke(conversationHistory)
    conversationHistory.append(response)
    return response.content

def get_history_for_frontend():
    """Convert conversation history to a list of dicts for the frontend."""
    messages = []
    for msg in conversationHistory:
        if isinstance(msg, SystemMessage):
            messages.append({"role": "system", "content": msg.content})
        elif isinstance(msg, HumanMessage):
            messages.append({"role": "human", "content": msg.content})
        elif isinstance(msg, AIMessage):
            messages.append({"role": "ai", "content": msg.content})
    return messages

def reset_conversation():
    """Clear conversation history and start fresh."""
    global conversationHistory
    conversationHistory = [SystemMessage(content=SYSTEM_PROMPT)]

# ============================================================
# Flask Web Server
# ============================================================
app = Flask(__name__, static_folder="static")

@app.route("/")
def index():
    """Serve the chat HTML page."""
    return send_from_directory("static", "index.html")

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """API endpoint: receives user message, returns AI response."""
    data = request.get_json()
    user_message = data.get("message", "").strip()
    
    if not user_message:
        return jsonify({"error": "Empty message"}), 400
    
    try:
        ai_response = chat_with_llm(user_message)
        return jsonify({"response": ai_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/history", methods=["GET"])
def api_history():
    """API endpoint: returns full conversation history."""
    return jsonify({"history": get_history_for_frontend()})

@app.route("/api/reset", methods=["POST"])
def api_reset():
    """API endpoint: resets the conversation."""
    reset_conversation()
    return jsonify({"status": "reset", "history": get_history_for_frontend()})

# ============================================================
# Start the server
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  iOS INTERVIEW CHAT - Web UI")
    print("  Open http://localhost:5050 in your browser")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5050, debug=False)