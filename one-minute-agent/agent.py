import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from .tools import tools

with open("agent/prompt.md", "r") as file:
    prompt = file.read()

root_agent = Agent(
    name="emergency_911_agent",
    model="gemini-2.0-flash",
    description=(
        "AI agent that communicates with 911 operators on behalf of a person experiencing an emergency."
    ),
    instruction=prompt,
    tools=tools,
)