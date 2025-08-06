# Multi-stage build for React + FastAPI deployment
FROM node:18-alpine AS frontend-builder

# Build React frontend
WORKDIR /app/frontend
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Python backend stage
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire one-minute-agent project
COPY ../one_minute_agent ./one_minute_agent
COPY ../nagents ./nagents
COPY ../medical_kb ./medical_kb

# Copy React build from frontend stage
COPY --from=frontend-builder /app/frontend/dist ./static

# Copy FastAPI server
COPY server.py .

# Create startup script
COPY start.sh .
RUN chmod +x start.sh

# Expose port (Hugging Face Spaces uses 7860)
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1

# Start the application
CMD ["./start.sh"] 