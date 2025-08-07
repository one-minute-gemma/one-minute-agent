#!/bin/bash
set -e

# Print Ollama version
echo "🔍 Checking Ollama version:"
ollama --version

# Start Ollama service in the background
echo "🚀 Starting Ollama service on $OLLAMA_HOST..."
nohup ollama serve > /tmp/ollama.log 2>&1 &
OLLAMA_PID=$!

# Give Ollama time to start
echo "⏳ Waiting for Ollama to start (15 seconds)..."
sleep 15

# Check if Ollama is running
if ps -p $OLLAMA_PID > /dev/null; then
    echo "✅ Ollama service running with PID: $OLLAMA_PID"
else
    echo "❌ Ollama service failed to start. Check /tmp/ollama.log for details:"
    cat /tmp/ollama.log
    echo "⚠️ Continuing anyway..."
fi

# Pull the model (with increased timeout)
echo "📦 Pulling model gemma3n:e2b (this may take a while)..."
timeout 600 ollama pull gemma3n:e2b || echo "⚠️ Model pull timed out or failed, continuing anyway..."

# Start Streamlit
echo "🌐 Starting Streamlit app..."
exec uv run streamlit run streamlit/streamlit_app.py --server.port=8501 --server.address=0.0.0.0