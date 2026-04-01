# ══════════════════════════════════════════════════════════════
# FILE: test_api.py
# Run: python test_api.py  (from any folder, with my-adk active)
# ══════════════════════════════════════════════════════════════

import requests
import json

BASE_URL = "http://localhost:8000"
APP_NAME = "multi_tool_agent"   # ← your folder name
USER_ID  = "user_001"           # ← can be any string

# ── STEP 1: Create a new session ─────────────────────────────
print("📌 Creating session...")

session_response = requests.post(
    f"{BASE_URL}/apps/{APP_NAME}/users/{USER_ID}/sessions",
    headers={"Content-Type": "application/json"},
    json={}
)

session_id = session_response.json()["id"]   # extract the session ID
print(f"   ✅ Session created: {session_id}")

# ── STEP 2: Send a message to the agent ───────────────────────
print("\n📌 Asking agent: 'What is the weather and time in New York?'")

run_response = requests.post(
    f"{BASE_URL}/apps/{APP_NAME}/users/{USER_ID}/sessions/{session_id}/run",
    headers={"Content-Type": "application/json"},
    json={
        "app_name": APP_NAME,
        "user_id":  USER_ID,
        "session_id": session_id,
        "new_message": {
            "role": "user",
            "parts": [{"text": "What is the weather and time in New York?"}]
        }
    }
)

# ── STEP 3: Extract and print the final text reply ─────────────
events = run_response.json()  # ADK returns a list of events

for event in events:
    # Each event has a 'content' with parts
    if event.get("content") and event["content"].get("parts"):
        for part in event["content"]["parts"]:
            if part.get("text"):  # only print text parts (not tool calls)
                print(f"\n🤖 Agent: {part['text']}")