"""
OneMinute Emergency Agent - Simple Implementation

A simple demonstration of the nagents framework for emergency scenarios.
Uses configuration from config/config.py
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from .config.config import config
from nagents import ToolRegistry, OllamaProvider, ToolExecutor
from .agent import OneMinuteAgent
from .tools import emergency_tools

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

def main():
    """Simple example of emergency agent usage"""
    
    print("🚨 Creating Emergency Agent...")
    agent = create_emergency_agent(show_thinking=True)
    
    while True:
        user_input = input("911 Operator: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            break
            
        result = agent.chat(user_input)
        print(f"OneMinute Agent: {result.content}")
        
        if result.tools_executed:
            print(f"Tools used: {len(result.tools_executed)}")
        if result.metadata:
            print(f"Metadata: {result.metadata}")

if __name__ == "__main__":
    main() 