"""
OneMinute Emergency Agent - Simple Implementation

A simple demonstration of the nagents framework for emergency scenarios.
Uses the new agent factory system with proper tool organization.
"""
import sys
import logging
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from .config.config import config
from nagents import OllamaProvider
from .agents import create_agent, create_operator_agent, create_victim_assistant_agent, AgentType

def create_emergency_agent(
        agent_type: AgentType = "operator",
        model_name: str = "gemma3n:e2b", 
        show_thinking: bool = False, 
        max_iterations: int = 2,
        always_use_reasoning: bool = True
        ):
    """
    Create a ready-to-use emergency agent.
    
    Args:
        agent_type: Type of agent ("operator" or "victim-assistant")
        model_name: Ollama model to use (default: gemma3n:e2b)
        show_thinking: Whether to show the agent's reasoning process
        max_iterations: Maximum reasoning iterations
        
    Returns:
        Configured emergency agent with appropriate tools
    """
    
    model_provider = OllamaProvider(model_name)
    
    # Use the factory system - handles tool registration automatically
    agent = create_agent(
        agent_type=agent_type,
        model_provider=model_provider,
        max_iterations=max_iterations,
        show_thinking=show_thinking,
        always_use_reasoning=always_use_reasoning
    )
    
    return agent

# Convenience function for operator agent
def create_operator_emergency_agent(model_name: str = "gemma3n:e2b", show_thinking: bool = False, max_iterations: int = 2):
    """Create a 911 operator communication agent."""
    model_provider = OllamaProvider(model_name)
    return create_operator_agent(model_provider, max_iterations, show_thinking)

def main():
    """Interactive demo with agent type selection"""
    
    print("🚨 OneMinute Emergency Response System")
    print("=====================================")
    print("1. Operator Agent - Communicates with 911 dispatchers")
    print("2. Victim Assistant Agent - Provides direct help to victims")
    print()
    
    choice = input("Select agent type (1 for Operator, 2 for Victim Assistant): ").strip()
    
    if choice == "1":
        agent_type = "operator"
        agent_name = "911 Operator Agent"
        prompt_prefix = "911 Operator: "
        max_iter = 2
    elif choice == "2":
        agent_type = "victim-assistant" 
        agent_name = "Victim Assistant Agent"
        prompt_prefix = "Emergency Victim: "
        max_iter = 3
    else:
        print("Invalid choice, defaulting to Operator Agent")
        agent_type = "operator"
        agent_name = "911 Operator Agent" 
        prompt_prefix = "911 Operator: "
        max_iter = 2
    
    print(f"\n🚨 Creating {agent_name}...")
    agent = create_emergency_agent(
        agent_type=agent_type,
        show_thinking=True,
        max_iterations=max_iter
    )
    
    print(f"✅ {agent_name} ready!")
    print("Type 'quit', 'exit', or 'bye' to end the conversation.\n")
    
    while True:
        user_input = input(prompt_prefix)
        if user_input.lower() in ['quit', 'exit', 'bye']:
            break
            
        result = agent.chat(user_input)
        print(f"{agent_name}: {result.content}")
        
        if result.tools_executed:
            print(f"🔧 Tools used: {len(result.tools_executed)}")
        if result.metadata:
            print(f"📊 Metadata: {result.metadata}")
        print()

if __name__ == "__main__":
    main() 