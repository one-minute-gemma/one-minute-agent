# Nagents - Examples

This directory contains example agents built with the Nagents Agent Framework. Each example demonstrates different use cases and patterns for building intelligent agents with local models.

## Available Examples

### 🚨 Emergency Agent (`emergency/`)
A specialized agent for 911 emergency response scenarios.

**Features:**
- Fast decision-making (max 2 tool calls)
- Emergency-specific reasoning patterns
- Health monitoring, location tracking, audio/video analysis
- Optimized for life-critical scenarios

**Usage:**
```python
from ollama_agent.examples.emergency import create_emergency_agent

agent = create_emergency_agent(show_thinking=True)
result = agent.chat("911 what's your emergency?")
print(result["response"])
```

## Creating Your Own Example

1. **Create a new directory**: `my_agent/`
2. **Create your agent**: `my_agent/agent.py`
3. **Define your tools**: `my_agent/tools.py` 
4. **Add convenience function**: `my_agent/__init__.py`

### Example Structure:
```
my_agent/
├── __init__.py          # Export create_my_agent()
├── agent.py            # MyAgent(BaseAgent)
├── tools.py            # List of tool functions
└── prompts/            # Agent-specific prompts
    └── system.md
```

### Minimal Agent:
```python
# my_agent/agent.py
from ollama_agent import BaseAgent

class MyAgent(BaseAgent):
    def should_use_reasoning_loop(self, user_input):
        return "help" in user_input.lower()
    
    def build_system_prompt(self):
        return "You are a helpful assistant."
    
    def parse_reasoning_response(self, response):
        # Your parsing logic
        pass
    
    def parse_final_response(self, response):
        return response.strip()
```

### Simple Tools:
```python
# my_agent/tools.py  
def my_tool(query: str) -> dict:
    """A simple tool that processes queries"""
    return {"result": f"Processed: {query}"}

tools = [my_tool]
```

### Easy Import:
```python
# my_agent/__init__.py
from ollama_agent import ToolRegistry, ToolExecutor, ToolProvider
from ollama_agent.providers import OllamaProvider
from .agent import MyAgent
from .tools import tools

def create_my_agent(model_name="gemma3n:e2b"):
    registry = ToolRegistry()
    provider = ToolProvider()
    tool_defs = provider.get_tools(tools, "custom")
    for tool in tool_defs:
        registry.register_tool(tool)
    
    return MyAgent(
        model_provider=OllamaProvider(model_name),
        tool_executor=ToolExecutor(registry)
    )
```

## Future Examples (Ideas)

- **Customer Service Agent**: Handle support tickets with knowledge base access
- **Coding Assistant**: Help with code generation and debugging  
- **Research Agent**: Gather information from multiple sources
- **Education Tutor**: Adaptive learning with progress tracking
- **Legal Assistant**: Document analysis and case research

## Contributing

Want to add your own example? 

1. Follow the structure above
2. Make it self-contained
3. Add clear documentation
4. Test with different local models
5. Submit a PR!

The goal is to showcase the versatility of the Nagents Agent Framework across different domains. 