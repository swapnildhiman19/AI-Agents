# IBM-AI environment setup

This folder contains everything needed to recreate the **ibm-ai** conda environment on a new machine (e.g. after cloning the repo elsewhere).

## What’s included

| File | Purpose |
|------|--------|
| **requirements.txt** | Full list of pip packages (and versions) from the current `ibm-ai` env. |
| **setup_ibm_ai_env.sh** | Script that creates the conda env and runs `pip install -r requirements.txt`. |
| **ENV_SETUP.md** | This file — manual steps and notes. |

## Option A: One-command setup (recommended)

From the **IBM-AI** directory:

```bash
chmod +x setup_ibm_ai_env.sh
./setup_ibm_ai_env.sh
```

Then activate and (if needed) add your API key:

```bash
conda activate ibm-ai
# Copy .env.example to .env and set GOOGLE_API_KEY where you use Gemini (e.g. IBM-Rag-And-Agentic)
```

## Option B: Manual steps

1. **Create the conda environment**
   ```bash
   conda create -n ibm-ai python=3.11 -y
   conda activate ibm-ai
   ```

2. **Install dependencies**
   ```bash
   cd /path/to/AI-Agents/IBM-AI
   pip install -r requirements.txt
   ```

3. **Environment variables**  
   Where the code uses Google Gemini (or other APIs), set keys in a `.env` file (e.g. `IBM-Rag-And-Agentic/.env`) and ensure `.env` is in `.gitignore` so it isn’t committed.

## Regenerating requirements.txt (on this machine)

If you add or remove packages in `ibm-ai` and want to update the snapshot:

```bash
conda activate ibm-ai
pip freeze | grep -v '@ file://' | grep -v '@ file:' > requirements.txt
```

Then commit the updated `requirements.txt` so others (or you on another machine) can stay in sync.

## Notes

- **Python**: Environment was captured with **Python 3.11**. The script creates the env with `python=3.11`.
- **Conda**: The script assumes `conda` is on your PATH (Miniconda/Anaconda installed).
- **Platform**: Versions in `requirements.txt` are from the machine where the env was exported; on a different OS/arch, pip may resolve slightly different wheels, but behavior should match.
