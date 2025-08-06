"""
Agent Factory for One Minute Emergency Response System
"""

from typing import Literal
from nagents.base.tool_registry import ToolExecutor, ToolRegistry

from .operator.agent import OneMinuteAgent
from .operator.tools import emergency_tools as operator_tools

from .victim_assistant.agent import VictimAssistantAgent
from .victim_assistant.tools import victim_assitant_tools as victim_tools

# Import communication tools
from ..communication.communication_tools import (
    create_victim_communication_tools,
    create_operator_communication_tools
)
from ..communication.coordination_system import get_coordination_system
from ..communication.message_types import AgentRole

AgentType = Literal["operator", "victim-assistant"]


def create_agent(
    agent_type: AgentType,
    model_provider,
    max_iterations: int = 3,
    show_thinking: bool = False,
    always_use_reasoning: bool = True,
    enable_communication: bool = True
):
    """
    Create an emergency response agent with appropriate tools.
    
    Args:
        agent_type: Type of agent to create ("operator" or "victim-assistant")
        model_provider: Model provider for the agent
        max_iterations: Maximum reasoning iterations
        show_thinking: Whether to show agent's internal reasoning
        enable_communication: Whether to enable inter-agent communication tools
        
    Returns:
        Configured emergency response agent
    """
    
    if agent_type == "operator":
        registry = ToolRegistry()
        
        # Register operator tools
        for tool in operator_tools:
            registry.register_tool(tool)
        
        # Register communication tools if enabled
        if enable_communication:
            comm_tools = create_operator_communication_tools()
            for tool in comm_tools:
                registry.register_tool(tool)
        
        # Create tool executor with operator tools
        tool_executor = ToolExecutor(registry)
        
        agent = OneMinuteAgent(
            model_provider=model_provider,
            tool_executor=tool_executor,
            max_iterations=max_iterations,
            show_thinking=show_thinking,
            always_use_reasoning=always_use_reasoning
        )
        
        # Register agent with coordination system if communication is enabled
        if enable_communication:
            coordination_system = get_coordination_system()
            coordination_system.register_agent(AgentRole.OPERATOR, agent)
        
        return agent
        
    elif agent_type == "victim-assistant":
        registry = ToolRegistry()

        for tool in victim_tools:
            registry.register_tool(tool)

        # Register communication tools if enabled
        if enable_communication:
            comm_tools = create_victim_communication_tools()
            for tool in comm_tools:
                registry.register_tool(tool)

        # Create tool executor with victim assistant tools
        tool_executor = ToolExecutor(registry)
        
        agent = VictimAssistantAgent(
            model_provider=model_provider,
            tool_executor=tool_executor,
            max_iterations=max_iterations,
            show_thinking=show_thinking,
            always_use_reasoning=always_use_reasoning
        )
        
        # Register agent with coordination system if communication is enabled
        if enable_communication:
            coordination_system = get_coordination_system()
            coordination_system.register_agent(AgentRole.VICTIM_ASSISTANT, agent)
        
        return agent


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