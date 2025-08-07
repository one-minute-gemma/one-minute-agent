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
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Download and install Ollama (as root)
# Using specific version v0.11.3 from GitHub
RUN mkdir -p /opt/ollama && \
    wget -q -O /opt/ollama/ollama https://github.com/ollama/ollama/releases/download/v0.11.3/ollama-linux-amd64 && \
    chmod +x /opt/ollama/ollama && \
    chown -R app:app /opt/ollama

# Switch to non-root user
USER app

# Set uv cache directory to a writable location
ENV UV_CACHE_DIR=/app/.uv-cache
ENV UV_PROJECT_ENVIRONMENT=/app/.venv

# Set environment for Ollama
ENV PATH="$PATH:/opt/ollama"
ENV OLLAMA_HOST="0.0.0.0:11434"

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