"""
Agent Factory for One Minute Emergency Response System
"""

from typing import Literal
from nagents.base.tool_registry import ToolExecutor, ToolRegistry

from .operator.agent import OneMinuteAgent
from .operator.tools import emergency_tools as operator_tools

from .victim_assistant.agent import VictimAssistantAgent
from .victim_assistant.tools import victim_assitant_tools as victim_tools

AgentType = Literal["operator", "victim-assistant"]


def create_agent(
    agent_type: AgentType,
    model_provider,
    max_iterations: int = 3,
    show_thinking: bool = False,
    always_use_reasoning: bool = True
):
    """
    Create an emergency response agent with appropriate tools.
    
    Args:
        agent_type: Type of agent to create ("operator" or "victim-assistant")
        model_provider: Model provider for the agent
        max_iterations: Maximum reasoning iterations
        show_thinking: Whether to show agent's internal reasoning
        
    Returns:
        Configured emergency response agent
    """
    
    if agent_type == "operator":
        registry = ToolRegistry()
        
        # Register operator tools
        for tool in operator_tools:
            registry.register_tool(tool)
        
        # Create tool executor with operator tools
        tool_executor = ToolExecutor(registry)
        
        return OneMinuteAgent(
            model_provider=model_provider,
            tool_executor=tool_executor,
            max_iterations=max_iterations,
            show_thinking=show_thinking,
            always_use_reasoning=always_use_reasoning
        )
        
    elif agent_type == "victim-assistant":
        registry = ToolRegistry()

        for tool in victim_tools:
            registry.register_tool(tool)

        # Create tool executor with victim assistant tools
        tool_executor = ToolExecutor(registry)
        
        
        return VictimAssistantAgent(
            model_provider=model_provider,
            tool_executor=tool_executor,
            max_iterations=max_iterations,
            show_thinking=show_thinking,
            always_show_reasoning=always_use_reasoning
        )


# Convenience functions
def create_operator_agent(model_provider, max_iterations: int = 2, show_thinking: bool = False):
    """Create a 911 operator communication agent."""
    return create_agent("operator", model_provider, max_iterations, show_thinking)


def create_victim_assistant_agent(model_provider, max_iterations: int = 3, show_thinking: bool = False):
    """Create a victim assistance agent."""
    return create_agent("victim-assistant", model_provider, max_iterations, show_thinking)


__all__ = [
    'create_agent',
    'create_operator_agent', 
    'create_victim_assistant_agent',
    'AgentType'
] 