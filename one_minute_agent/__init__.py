"""
One Minute Emergency Response Agent System

Provides two specialized agents:
- Operator Agent: Communicates with 911 dispatchers  
- Victim Assistant Agent: Provides direct help to emergency victims
"""

from .agents import (
    create_agent,
    create_operator_agent,
    create_victim_assistant_agent,
    AgentType
)

# Also expose individual agent classes for advanced usage
from .agents.operator.agent import OneMinuteAgent
from .agents.victim_assistant.agent import VictimAssistantAgent

__all__ = [
    # Factory functions (recommended usage)
    'create_agent',
    'create_operator_agent', 
    'create_victim_assistant_agent',
    'AgentType',
    
    # Individual agent classes (advanced usage)
    'OneMinuteAgent',
    'VictimAssistantAgent'
]
