"""
OneMinuteAgent - An agent designed to help people suffering emergencies
by communicating with 911 operators. 

Main exports for frontend integration:
- OneMinuteAgentAPI: Main API class
- create_emergency_agent: Quick setup function
- create_custom_emergency_agent: Custom setup function

Example usage:
    from ollama_agent import create_emergency_agent
    
    agent = create_emergency_agent()
    result = agent.chat("911 what's your emergency?")
    print(result["response"])
"""


from .api import (
    OneMinuteAgentAPI,
    create_emergency_agent,
    create_custom_emergency_agent
)

# Base classes for advanced usage
from .base.agent import BaseAgent, AgentResponse, Message
from .base.tool_registry import ToolRegistry, ToolExecutor, ToolDefinition, ToolProvider

# Providers for different model backends
from .providers.ollama_provider import OllamaProvider

# Emergency-specific components
from .agents.emergency_agent import OneMinuteAgent
from .tools.emergency_tools import ToolProvider

__version__ = "1.0.0"
__author__ = "OneMinuteAgent System"

# Convenience aliases for TypeScript-like naming
Agent = BaseAgent
Response = AgentResponse
Registry = ToolRegistry
Executor = ToolExecutor

__all__ = [
    # Main API - Frontend developers use these
    "OneMinuteAgentAPI",
    "create_emergency_agent", 
    "create_custom_emergency_agent",
    
    # Base classes - For advanced customization
    "BaseAgent", "Agent",
    "AgentResponse", "Response", 
    "Message",
    "ToolRegistry", "Registry",
    "ToolExecutor", "Executor",
    "ToolDefinition",
    "ToolProvider",
    
    # Providers - For different model backends
    "OllamaProvider",
    
    # Emergency-specific
    "OneMinuteAgent",
    "ToolProvider",
]
