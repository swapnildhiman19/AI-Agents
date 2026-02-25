#!/usr/bin/env bash
# =============================================================================
# Setup script for the IBM-AI conda environment
# Run this on a new machine to recreate the ibm-ai environment and install
# all dependencies used in this repository (LangChain, Gemini, RAG, etc.).
#
# Prerequisites: Miniconda or Anaconda installed
# Usage: ./setup_ibm_ai_env.sh   (from the IBM-AI folder)
#    or: bash setup_ibm_ai_env.sh
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQUIREMENTS="${SCRIPT_DIR}/requirements.txt"

if [[ ! -f "$REQUIREMENTS" ]]; then
    echo "Error: requirements.txt not found at $REQUIREMENTS"
    exit 1
fi

# Check for conda
if ! command -v conda &> /dev/null; then
    echo "Error: conda not found. Please install Miniconda or Anaconda first."
    echo "  https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

echo "Creating conda environment 'ibm-ai' with Python 3.11..."
conda create -n ibm-ai python=3.11 -y

echo ""
echo "Installing pip dependencies from requirements.txt..."
conda run -n ibm-ai pip install -r "$REQUIREMENTS"

echo ""
echo "Done. Activate the environment with:"
echo "  conda activate ibm-ai"
echo ""
echo "Then set your GOOGLE_API_KEY in the .env file where needed (e.g. IBM-Rag-And-Agentic/.env)."
