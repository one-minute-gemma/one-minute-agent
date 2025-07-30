from google.adk.agents import Agent
from .tools.tools import (
    get_health_metrics,
    get_user_location,
    get_audio_input,
    get_video_input,
    get_user_details,
)

AGENT_MODEL = "gemini-2.0-flash"

with open("one-minute-agent/utils/video_agent_prompt.md", "r") as file:
    video_prompt = file.read()

with open("one-minute-agent/utils/audio_agent_prompt.md", "r") as file:
    audio_prompt = file.read()

with open("one-minute-agent/utils/conversation_agent_prompt.md", "r") as file:
    conversation_prompt = file.read()

with open("one-minute-agent/utils/root_agent_prompt.md", "r") as file:
    root_prompt = file.read()

video_agent = Agent(
    name="video_agent",
    model=AGENT_MODEL,
    description="Specialized agent that analyzes video input to provide visual emergency scene assessment.",
    instruction=video_prompt,
    tools=[get_video_input],
)

audio_agent = Agent(
    name="audio_agent",
    model=AGENT_MODEL,
    description="Specialized agent that analyzes audio input to interpret speech and vocal distress indicators.",
    instruction=audio_prompt,
    tools=[get_audio_input],
)

conversation_agent = Agent(
    name="conversation_agent",
    model=AGENT_MODEL,
    description="Specialized agent that coordinates and synthesizes information from multiple emergency data sources.",
    instruction=conversation_prompt,
)

root_agent = Agent(
    name="emergency_911_agent",
    model=AGENT_MODEL,
    description=(
        "Primary AI agent that communicates with 911 operators, coordinating sub-agents and tools to provide comprehensive emergency information."
    ),
    instruction=root_prompt,
    sub_agents=[video_agent, audio_agent, conversation_agent],
    tools=[
        get_health_metrics,
        get_user_location,
        get_user_details,
    ],
)