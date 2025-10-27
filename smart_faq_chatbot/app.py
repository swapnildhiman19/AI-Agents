import os
import json
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load your Indian cities data
with open('data/indian_cities.json', 'r') as f:
    cities_data = json.load(f)

def create_context():
    """Create context from your cities data"""
    context = "You are a helpful travel assistant for Indian cities. Here's information about some popular destinations:\n\n"
    for city in cities_data[:5]:  # Use first 5 cities
        context += f"**{city['name']}**: {city['shortDescription']}\n"
    return context

def ask_llm(question, context):
    """Send question to your local LLM"""
    try:
        payload = {
            "model": os.getenv("LLM_MODEL"),
            "messages": [
                {"role": "system", "content": context},
                {"role": "user", "content": question}
            ],
            "max_tokens": 150,
            "temperature": 0.7
        }
        
        response = requests.post(
            os.getenv("LLM_BASE_URL"),
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return "Sorry, I'm having trouble connecting to my brain right now."
            
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get('question', '')
    if not user_question:
        return jsonify({"error": "No question provided"}), 400
    
    context = create_context()
    answer = ask_llm(user_question, context)
    
    return jsonify({
        "question": user_question,
        "answer": answer
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)