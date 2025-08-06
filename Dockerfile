FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy uv configuration files
COPY pyproject.toml uv.lock ./

# Copy the entire project (needed for imports in streamlit app)
COPY . .

# Install dependencies using uv
RUN uv sync --frozen

# Expose the streamlit port
EXPOSE 8501

# Health check for streamlit
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Use uv to run the streamlit app
ENTRYPOINT ["uv", "run", "streamlit", "run", "streamlit/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]