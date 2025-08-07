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

# Wait for Ollama API (up to 60s)
echo "⏳ Waiting for Ollama API to become ready..."
READY=0
for i in {1..12}; do
  if curl -s -m 5 http://localhost:11434/api/version >/dev/null; then
    READY=1
    break
  fi
  echo "... not ready yet ($i/12)"
  sleep 5
done

if [ "$READY" -eq 1 ]; then
  echo "✅ Ollama API is ready"
else
  echo "⚠️ Ollama API not ready after waiting, continuing anyway..."
fi

# Pull the model (with increased timeout)
echo "📦 Pulling model gemma3n:e2b (this may take a while)..."
if ! timeout 1200 ollama pull gemma3n:e2b; then
  echo "⚠️ Model pull timed out or failed, continuing anyway..."
fi

# Verify model presence
echo "🔎 Verifying model availability..."
if ollama list | grep -q "gemma3n:e2b"; then
  echo "✅ Model gemma3n:e2b is available"
else
  echo "⚠️ Model gemma3n:e2b not found locally yet"
fi

# Warm up the model to reduce first-request latency (keep alive for 10 minutes)
echo "🔥 Warming up model (short generate)..."
WARMUP_PAYLOAD='{"model":"gemma3n:e2b","prompt":"warmup","stream":false,"options":{"num_predict":8,"temperature":0},"keep_alive":"10m"}'
if timeout 300 curl -s -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d "$WARMUP_PAYLOAD" >/tmp/ollama_warmup.json; then
  echo "✅ Warmup completed"
else
  echo "⚠️ Warmup timed out or failed, continuing anyway..."
fi

# Start Streamlit
echo "🌐 Starting Streamlit app..."
exec uv run streamlit run streamlit/streamlit_app.py --server.port=8501 --server.address=0.0.0.0