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

# Expose the streamlit port
EXPOSE 8501

# Health check for streamlit
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Use uv to run the streamlit app
ENTRYPOINT ["uv", "run", "streamlit", "run", "streamlit/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]