# ADK Project

This project is managed using `uv`. 

## Setup & Running

1. **Environment Variables**:
   Fill in your Gemini or Google API key in the [.env](file:///Users/swapnildhiman/Desktop/AI/AI-Agents/ADK-Learning/ADK/ADK_Project/.env) file:
   ```env
   GEMINI_API_KEY="your_api_key_here"
   ```

2. **Run Scripts**:
   Always run Python scripts using `uv run`. This automatically executes them within the local virtual environment `.venv/` containing `google-adk` without needing to activate it manually:
   ```bash
   uv run python testing.py
   ```

3. **Install New Packages**:
   To add new dependencies to the project:
   ```bash
   uv add package_name
   ```
