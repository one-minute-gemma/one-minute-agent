#!/bin/bash
set -e

# Print system info
echo "📊 System information:"
uname -a
echo "Memory:"
free -h

# Create model directory if it doesn't exist
mkdir -p /app/.ollama/models

# Print Ollama version
echo "🔍 Checking Ollama version:"
ollama --version

# Verify Ollama binary
if [ -f "/usr/local/bin/ollama" ]; then
    echo "✅ Ollama binary found at /usr/local/bin/ollama"
    ls -la /usr/local/bin/ollama
    file /usr/local/bin/ollama
else
    echo "❌ Ollama binary not found at /usr/local/bin/ollama"
    which ollama || echo "ollama not found in PATH"
fi

# Start Ollama service in the background
echo "🚀 Starting Ollama service on $OLLAMA_HOST..."
nohup ollama serve > /tmp/ollama.log 2>&1 &
OLLAMA_PID=$!

# Give Ollama time to start
echo "⏳ Waiting for Ollama to start (30 seconds)..."
sleep 30

# Check if Ollama is running
if ps -p $OLLAMA_PID > /dev/null; then
    echo "✅ Ollama service running with PID: $OLLAMA_PID"
else
    echo "❌ Ollama service failed to start. Check /tmp/ollama.log for details:"
    cat /tmp/ollama.log
    echo "⚠️ Continuing anyway..."
fi

# Check API connectivity
echo "🧪 Testing Ollama API connectivity..."
curl -s -m 5 http://localhost:11434/api/version || echo "⚠️ Failed to connect to Ollama API"

# Pull the model (with increased timeout)
echo "📦 Pulling model gemma3n:e2b (this may take a while)..."
timeout 600 ollama pull gemma3n:e2b || echo "⚠️ Model pull timed out or failed, continuing anyway..."

# Start Streamlit
echo "🌐 Starting Streamlit app..."
exec uv run streamlit run streamlit/streamlit_app.py --server.port=8501 --server.address=0.0.0.0