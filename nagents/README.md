# Nagents Framework

A framework system for building intelligent agents that work great with local models. Designed to make ReAct patterns and tool calling work seamlessly with smaller local models like Gemma, Llama, and others.

## 🎯 Philosophy

**Local-First**: Built from the ground up for local LLMs, not cloud APIs
**Framework-Agnostic**: Clean protocols and interfaces that work everywhere  
**TypeScript-Inspired**: Familiar patterns with Python's flexibility
**Production-Ready**: Robust error handling and structured responses

## 🚀 Quick Start

```python
from nagents import BaseAgent, ToolRegistry, ToolProvider, OllamaProvider

# 1. Define your tools
def get_weather(location: str) -> dict:
    """Get weather information for a location"""
    return {"location": location, "temperature": "72°F", "condition": "sunny"}

def search_web(query: str) -> dict:
    """Search the web for information"""
    return {"query": query, "results": ["Result 1", "Result 2"]}

# 2. Create and register tools
registry = ToolRegistry()
provider = ToolProvider()
tools = provider.get_tools([get_weather, search_web], domain="general")
for tool in tools:
    registry.register_tool(tool)

# 3. Create your custom agent
class MyAgent(BaseAgent):
    def should_use_reasoning_loop(self, user_input: str) -> bool:
        # Use reasoning for complex queries
        return any(word in user_input.lower() for word in ["search", "find", "weather", "help"])
    
    def build_system_prompt(self) -> str:
        return "You are a helpful assistant with access to weather and web search tools."

# 4. Initialize and use
from nagents.base.tool_registry import ToolExecutor

model_provider = OllamaProvider("gemma3n:e2b")
tool_executor = ToolExecutor(registry)
agent = MyAgent(model_provider, tool_executor, show_thinking=True)

# Chat with your agent
result = agent.chat("What's the weather like in San Francisco?")
print(result.content)
```

## 🏗️ Core Architecture

### Framework Components

```
nagents/
├── base/                     # Core framework
│   ├── agent.py             # BaseAgent class and protocols
│   └── tool_registry.py     # Tool system
├── providers/               # LLM providers
│   └── ollama_provider.py   # Ollama integration
├── examples/                # Example implementations
│   └── emergency/           # Emergency response agent
└── api.py                   # Frontend-friendly API
```

## 📦 Core Components

### BaseAgent

The foundation of all agents. Provides conversation management, reasoning loops, and tool coordination.

```python
from nagents import BaseAgent

class MyAgent(BaseAgent):
    def should_use_reasoning_loop(self, user_input: str) -> bool:
        """Determine if agent should use reasoning for this input"""
        return "complex" in user_input.lower()
    
    def build_system_prompt(self) -> str:
        """Build the system prompt for your agent"""
        return "You are a helpful assistant."
    
    def parse_reasoning_response(self, response: str) -> dict:
        """Parse LLM reasoning responses (implement your JSON parsing)"""
        return json.loads(response)
    
    def parse_final_response(self, response: str) -> str:
        """Parse final responses from the LLM"""
        return response.strip()
```

### Tool System

Automatically converts Python functions into callable tools for your agents.

```python
from nagents import ToolRegistry, ToolProvider, ToolExecutor

# Define tools as simple functions
def calculate(operation: str, a: float, b: float) -> dict:
    """Perform mathematical calculations"""
    if operation == "add":
        return {"result": a + b}
    elif operation == "multiply":
        return {"result": a * b}
    else:
        return {"error": "Unsupported operation"}

# Convert to tools
provider = ToolProvider()
tools = provider.get_tools([calculate], domain="math")

# Register and execute
registry = ToolRegistry()
for tool in tools:
    registry.register_tool(tool)

executor = ToolExecutor(registry)
result = executor.execute("calculate", {"operation": "add", "a": 5, "b": 3})
print(result)  # {"result": 8}
```

### Model Providers

Clean interfaces for different LLM providers.

```python
from nagents import OllamaProvider

# Ollama (local models)
provider = OllamaProvider("gemma3n:e2b")

# Easy to extend for other providers
class CustomProvider:
    def chat(self, messages, system_prompt):
        # Your implementation
        return "response"
```

## 🛠️ Advanced Usage

### Reasoning Patterns

Agents can use structured reasoning loops for complex tasks:

```python
class ReasoningAgent(BaseAgent):
    def should_use_reasoning_loop(self, user_input: str) -> bool:
        # Use reasoning for multi-step tasks
        complex_indicators = ["analyze", "plan", "research", "find", "calculate"]
        return any(indicator in user_input.lower() for indicator in complex_indicators)
    
    def parse_reasoning_response(self, response: str) -> dict:
        """Parse structured reasoning responses"""
        try:
            parsed = json.loads(response.strip())
            return {
                "thought": parsed.get("thought", ""),
                "action": parsed.get("action", "None"),
                "actionInput": parsed.get("actionInput", {})
            }
        except json.JSONDecodeError:
            # Fallback parsing for malformed JSON
            return self._parse_malformed_response(response)
```

### Custom Tool Providers

Create specialized tool collections:

```python
from nagents.base.tool_registry import ToolProvider

class DatabaseToolProvider(ToolProvider):
    """Provider for database-related tools"""
    
    def get_tools(self, functions, domain="database"):
        # Custom tool processing for database functions
        tools = []
        for func in functions:
            tool_def = self._create_database_tool(func)
            tools.append(tool_def)
        return tools
```

### Error Handling

Built-in robust error handling:

```python
# Agents automatically handle errors and provide fallback responses
result = agent.chat("Complex query that might fail")

if result.metadata and "error" in result.metadata:
    print(f"Error occurred: {result.metadata['error']}")
else:
    print(f"Success: {result.content}")
    print(f"Tools used: {len(result.tools_executed)}")
```

## 📚 Examples

### Emergency Response Agent

```python
from nagents.examples.emergency import create_emergency_agent

# Pre-built emergency agent with health monitoring, location, etc.
agent = create_emergency_agent(
    model_name="gemma3n:e2b",
    show_thinking=True,
    max_iterations=2
)

result = agent.chat("911 what's your emergency?")
print(result.content)
```

### Run Example from Command Line

```bash
# Run the emergency example
python -m nagents
```

## 🎨 Creating Custom Agents

### 1. Minimal Agent

```python
from nagents import BaseAgent

class SimpleAgent(BaseAgent):
    def should_use_reasoning_loop(self, user_input: str) -> bool:
        return False  # Always use simple responses
    
    def build_system_prompt(self) -> str:
        return "You are a simple chatbot."
```

### 2. Task-Specific Agent

```python
class CodingAgent(BaseAgent):
    def should_use_reasoning_loop(self, user_input: str) -> bool:
        coding_keywords = ["code", "debug", "function", "class", "error"]
        return any(keyword in user_input.lower() for keyword in coding_keywords)
    
    def build_system_prompt(self) -> str:
        tools_info = ""
        if self.tool_executor:
            tools = self.tool_executor.get_available_tools()
            tools_info = f"Available tools: {', '.join(tools.keys())}"
        
        return f"""You are a coding assistant.
        
{tools_info}

When you need to use tools, respond with JSON:
{{"thought": "your reasoning", "action": "tool_name", "actionInput": {{}}}}

When you have enough information, respond with:
{{"thought": "I have sufficient information", "action": "None", "actionInput": {{}}}}
        """
```

### 3. Domain-Specific Tools

```python
# Define domain-specific tools
def analyze_code(code: str, language: str = "python") -> dict:
    """Analyze code for potential issues"""
    return {
        "language": language,
        "lines": len(code.split('\n')),
        "suggestions": ["Consider adding type hints", "Add docstrings"]
    }

def run_tests(test_file: str) -> dict:
    """Run unit tests"""
    return {"status": "passed", "tests_run": 15, "failures": 0}

# Create agent with tools
registry = ToolRegistry()
provider = ToolProvider()
tools = provider.get_tools([analyze_code, run_tests], domain="coding")
for tool in tools:
    registry.register_tool(tool)

tool_executor = ToolExecutor(registry)
model_provider = OllamaProvider("gemma3n:e2b")

agent = CodingAgent(model_provider, tool_executor)
```

## 📖 API Reference

### BaseAgent

```python
class BaseAgent:
    def __init__(self, model_provider, tool_executor=None, max_iterations=3, show_thinking=False)
    def chat(self, user_input: str) -> AgentResponse
    def clear_conversation(self) -> None
    def get_conversation_history(self) -> List[Message]
    
    # Abstract methods to implement:
    def should_use_reasoning_loop(self, user_input: str) -> bool
    def build_system_prompt(self) -> str
    def parse_reasoning_response(self, response: str) -> dict
    def parse_final_response(self, response: str) -> str
```

### AgentResponse

```python
@dataclass
class AgentResponse:
    content: str                          # The agent's response
    tools_executed: List[Dict[str, Any]]  # Tools that were called
    metadata: Optional[Dict[str, Any]]    # Additional metadata
```

### ToolRegistry

```python
class ToolRegistry:
    def register_tool(self, tool: ToolDefinition) -> None
    def get_tool(self, name: str) -> Optional[ToolDefinition]
    def get_all_tools(self) -> Dict[str, ToolDefinition]
    def register_provider(self, provider: ToolProvider) -> None
```

## 🔧 Configuration

### Ollama Setup

1. Install [Ollama](https://ollama.ai/)
2. Pull a model: `ollama pull gemma3n:e2b`
3. Use in your agent: `OllamaProvider("gemma3n:e2b")`

### Recommended Models

- **gemma3n:e2b** - Fast, good for most tasks
- **llama3.1:8b** - Balanced performance
- **codellama:7b** - Code-specific tasks

## 🎯 Design Principles

### TypeScript-Like Patterns

- **Protocols**: Clear interfaces like TypeScript interfaces
- **Strong Typing**: Extensive type hints and validation
- **Composition**: Mix and match components easily

### Framework Agnostic

- Clean separation between agent logic and LLM providers
- Easy integration with web frameworks (FastAPI, Flask, etc.)
- Pluggable tool systems

### Local-First

- Optimized for local models with smaller context windows
- Efficient reasoning patterns that work with 7B-13B models
- No external API dependencies

## 🚀 Production Usage

### Web Integration

```python
from fastapi import FastAPI
from nagents.api import NagentsAPI

app = FastAPI()
nagents_api = NagentsAPI(model_name="gemma3n:e2b")

@app.post("/chat")
async def chat(message: str):
    result = nagents_api.chat(message)
    return result
```

### Error Handling

```python
try:
    result = agent.chat(user_input)
    if result.metadata and "error" in result.metadata:
        # Handle agent errors gracefully
        handle_error(result.metadata["error"])
    else:
        # Process successful response
        process_response(result.content)
except Exception as e:
    # Handle system errors
    logger.error(f"System error: {e}")
```

## 📝 Contributing

The framework is designed to be extensible. Common areas for contribution:

1. **New Model Providers**: Add support for other LLM providers
2. **Tool Categories**: Create specialized tool providers
3. **Agent Examples**: Build domain-specific agent examples
4. **Performance**: Optimize reasoning patterns for different model sizes

## 🔗 See Also

- [Emergency Agent Example](./examples/emergency/README.md)
- [Main Project README](../README.md)
- [One-Minute Agent Implementation](../one-minute-agent/README.md) 