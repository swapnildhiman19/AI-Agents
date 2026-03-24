import importlib.util
import os
import platform
import sys

# Load .env in this folder so GOOGLE_API_KEY / GEMINI_API_KEY are visible here
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

print("Python executable:", sys.executable)
print("Python:", sys.version)
print("Platform:", platform.platform())
print(
    "GOOGLE_API_KEY set:",
    bool(os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")),
)

# Package is installed as google-adk; import path is google.adk (not top-level "adk")
adk_spec = importlib.util.find_spec("google.adk")
print("ADK (google.adk) found:", bool(adk_spec))
if not adk_spec:
    print("Install in this env: pip install google-adk")
