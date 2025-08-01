from google.adk.agents import Agent
from google.adk.tools import agent_tool
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
    sub_agents=[],
    tools=[get_audio_input],
)

video_agent_tool = agent_tool.AgentTool(video_agent)
audio_agent_tool = agent_tool.AgentTool(audio_agent)

root_agent = Agent(
    name="emergency_911_agent",
    model=AGENT_MODEL,
    description=(
        "Primary AI agent that communicates with 911 operators, coordinating sub-agents and tools to provide comprehensive emergency information."
    ),
    instruction=root_prompt,
    tools=[
        get_health_metrics,
        get_user_location,
        get_user_details,
        video_agent_tool,
        audio_agent_tool,
    ],
)