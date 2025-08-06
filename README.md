---
title: One Minute Agent
emoji: 🚨
colorFrom: red
colorTo: yellow
sdk: docker
app_port: 8501
pinned: false
---

# One Minute Agent

An intelligent emergency response system built on the `nagents` framework. This project includes both a core agent framework (`nagents`) and a specialized emergency response agent (`one-minute-agent`) designed to assist during emergency situations by communicating with 911 operators.

## Project Structure

- **`nagents/`** - Core agent framework with base classes, tool registry, and provider system
- **`one-minute-agent/`** - Emergency response agent implementation 
- **`misc/`** - Legacy experimental code and samples

## Prerequisites

- Python 3.13+
- [Ollama](https://ollama.ai/) installed and running locally

## Quick Start

### 1. Setup Environment

```bash
# Create and activate virtual environment
uv venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync
```

### 2. Install Ollama Model

```bash
ollama pull gemma3n:e2b
```

### 3. Run the Emergency Agent

```bash
# Run the emergency response agent
python -m one-minute-agent

# OR run the framework example
python -m nagents
```

## Usage

The emergency agent simulates an AI monitoring system that communicates with 911 operators on behalf of a person experiencing an emergency. It can:

- Monitor health vitals and environmental conditions
- Assess emergency situations through audio/video analysis
- Provide location information to emergency responders
- Communicate clear, actionable information to 911 operators

## Configuration

The system uses Ollama for local LLM inference. Configuration can be found in `one-minute-agent/config/config.json`.

## Development

Each component has its own README with detailed information:
- See `nagents/README.md` for framework documentation
- See `one-minute-agent/README.md` for emergency agent specifics
