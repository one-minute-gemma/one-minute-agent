"""
Emergency Agent Example - 911 operator communication agent.

This example demonstrates how to build a specialized agent for emergency 
response scenarios using the Nagents Framework.

## Quick Usage:
```python
from nagents.examples.emergency import create_emergency_agent

agent = create_emergency_agent(show_thinking=True)
result = agent.chat("911 what's your emergency?")
print(result["response"])
```

## Components:
- OneMinuteAgent: Emergency-optimized agent with fast decision making
- emergency_tools: Pre-built tools for health, location, audio/video monitoring
"""

from .agent import OneMinuteAgent
from .tools import emergency_tools, tools

def create_emergency_agent(
        model_name: str = "gemma3n:e2b", 
        show_thinking: bool = False, 
        max_iterations: int = 2, 
        ):
    """
    Create a ready-to-use emergency agent.
    
    Args:
        model_name: Ollama model to use (default: gemma3n:e2b)
        show_thinking: Whether to show the agent's reasoning process
        
    Returns:
        Configured emergency agent ready for 911 operator communication
    """
    from ...base.tool_registry import ToolRegistry, ToolExecutor
    from ...providers.ollama_provider import OllamaProvider
    
    registry = ToolRegistry()

    for tool in emergency_tools:
        registry.register_tool(tool)
    
    model_provider = OllamaProvider(model_name)
    tool_executor = ToolExecutor(registry)
    
    agent = OneMinuteAgent(
        model_provider=model_provider,
        tool_executor=tool_executor,
        max_iterations=max_iterations,
        show_thinking=show_thinking
    )
    
    return agent

__all__ = [
    "OneMinuteAgent",
    "emergency_tools", 
    "tools",
    "create_emergency_agent"
] 