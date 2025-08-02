# One Minute Agent

This is an agent capable of helping a person experiencing an emergency.

## How to run

First, create a .env file in the one-minute-agent directory, containing the following variable:

````.env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=<your-google-studio-api-key>
````

From the root directory, run:

```bash
uv venv .venv
```

```bash
source .venv/bin/activate
```

```bash
uv sync
```

Then, run:

```bash
uv run run_agent.py                                                                        
```

This will open a web interface where you can interact with the agent.
