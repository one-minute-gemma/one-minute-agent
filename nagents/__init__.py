"""
Nagents - Build intelligent agents that work great with local models.

A TypeScript-like, framework-agnostic system for creating agentic workflows 
with local models like Gemma, Llama, etc. Designed to make ReAct patterns 
and tool calling work seamlessly with smaller local models.

## Core Components:
- BaseAgent: Extensible agent class with reasoning loops
- ToolRegistry: Auto-parse functions into tools 
- OllamaProvider: Local model integration
- Protocols: TypeScript-like interfaces for extensibility

## Quick Start:
```python
from ollama_agent import BaseAgent, ToolRegistry, ToolProvider

# Create tools
def my_tool():
    return {"result": "success"}

# Register tools  
registry = ToolRegistry()
provider = ToolProvider()
tools = provider.get_tools([my_tool], domain="custom")
for tool in tools:
    registry.register_tool(tool)

# Create custom agent
class MyAgent(BaseAgent):
    def should_use_reasoning_loop(self, user_input):
        return "help" in user_input.lower()
    
    def build_system_prompt(self):
        return "You are a helpful agent."
```

## Examples:
```python
# Emergency agent example
from ollama_agent.examples.emergency import create_emergency_agent
agent = create_emergency_agent()
```
"""

# Core framework components - main API
from .base.agent import BaseAgent, AgentResponse, Message
from .base.tool_registry import ToolRegistry, ToolExecutor, ToolDefinition, ToolProvider

# Model providers
from .providers.ollama_provider import OllamaProvider

__version__ = "1.0.0"
__author__ = "Nagents"

Agent = BaseAgent
Response = AgentResponse
Registry = ToolRegistry
Executor = ToolExecutor

__all__ = [
    # Core agent framework
    "BaseAgent", "Agent",
    "AgentResponse", "Response", 
    "Message",
    
    # Tool system
    "ToolRegistry", "Registry",
    "ToolExecutor", "Executor", 
    "ToolDefinition",
    "ToolProvider",
    
    # Model providers
    "OllamaProvider",
]

# Examples are imported separately:
# from ollama_agent.examples.emergency import create_emergency_agent
# from ollama_agent.examples.customer_service import create_support_agent  # Future
# from ollama_agent.examples.coding import create_coding_agent            # Future
