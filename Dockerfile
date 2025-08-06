FROM python:3.13-slim

WORKDIR /app

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Switch to non-root user
USER app

# Set uv cache directory to a writable location
ENV UV_CACHE_DIR=/app/.uv-cache
ENV UV_PROJECT_ENVIRONMENT=/app/.venv

# Copy uv configuration files
COPY --chown=app:app pyproject.toml uv.lock ./

# Copy the entire project (needed for imports in streamlit app)
COPY --chown=app:app . .

# Install dependencies using uv
RUN uv sync --frozen

# Download and setup Ollama with better error handling
RUN wget -O /app/ollama https://ollama.com/download/ollama-linux-amd64 && \
    chmod +x /app/ollama && \
    file /app/ollama

# Expose the streamlit port
EXPOSE 8501

# Health check for streamlit
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Create startup script with better error handling
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "🔧 Starting Ollama service..."\n\
./ollama serve &\n\
OLLAMA_PID=$!\n\
\n\
echo "⏳ Waiting for Ollama to start..."\n\
sleep 15\n\
\n\
echo "📦 Pulling model gemma3n:e2b..."\n\
if ./ollama pull gemma3n:e2b; then\n\
    echo "✅ Model pulled successfully"\n\
else\n\
    echo "❌ Failed to pull model, but continuing..."\n\
fi\n\
\n\
echo "🚀 Starting Streamlit..."\n\
uv run streamlit run streamlit/streamlit_app.py --server.port=8501 --server.address=0.0.0.0' > /app/start.sh && \
    chmod +x /app/start.sh

# Use the startup script
ENTRYPOINT ["/app/start.sh"]