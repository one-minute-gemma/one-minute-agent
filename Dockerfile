FROM python:3.13-slim

WORKDIR /app

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app

# Install system dependencies including packages needed for Ollama
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    wget \
    lsb-release \
    ca-certificates \
    procps \
    file \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install Ollama using the official install script (as root)
RUN curl -fsSL https://ollama.ai/install.sh | sh && \
    # Make sure Ollama is available in path
    ln -sf /usr/local/bin/ollama /usr/bin/ollama && \
    # Verify installation
    ls -la /usr/local/bin/ollama && \
    # Give access to app user
    chown app:app /usr/local/bin/ollama

# Switch to non-root user
USER app

# Set uv cache directory to a writable location
ENV UV_CACHE_DIR=/app/.uv-cache
ENV UV_PROJECT_ENVIRONMENT=/app/.venv

# Set environment for Ollama
ENV OLLAMA_HOST="0.0.0.0:11434"
# Set temporary model directory (will persist in the container)
ENV OLLAMA_MODELS="/app/.ollama/models"

# Copy uv configuration files
COPY --chown=app:app pyproject.toml uv.lock ./

# Copy the entire project (needed for imports in streamlit app)
COPY --chown=app:app . .

# Install dependencies using uv
RUN uv sync --frozen

# Expose the streamlit port and Ollama API port
EXPOSE 8501 11434

# Health check for streamlit
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Create startup script to run both Ollama and Streamlit
COPY --chown=app:app scripts/startup.sh /app/startup.sh
RUN chmod +x /app/startup.sh

# Use the startup script as entrypoint
ENTRYPOINT ["/app/startup.sh"]