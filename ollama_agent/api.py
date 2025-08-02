"""
Frontend-friendly API for the OneMinuteAgent system.
Provides a clean interface for creating and using one-minute agents.
"""
from typing import Optional, Dict, Any
from .base.agent import AgentResponse
from .base.tool_registry import ToolRegistry, ToolExecutor, default_registry
from .agents.emergency_agent import OneMinuteAgent
from .providers.ollama_provider import OllamaProvider
from .tools.emergency_tools import EmergencyToolsProvider

class OneMinuteAgentAPI:
    """
    Main API class for one-minute agent functionality.
    Designed to be easily pluggable into frontends.
    """
    
    def __init__(
        self, 
        model_name: str = "gemma3n:e2b",
        use_custom_registry: bool = False,
        show_thinking: bool = False
    ):
        """
        Initialize the OneMinuteAgent API.
        
        Args:
            model_name: Name of the Ollama model to use
            use_custom_registry: If True, creates a new registry. If False, uses global registry.
        """
        if use_custom_registry:
            self.registry = ToolRegistry()
        else:
            self.registry = default_registry
        
        if not any(tool.domain == "emergency" for tool in self.registry.tools.values()):
            emergency_provider = EmergencyToolsProvider()
            self.registry.register_provider(emergency_provider)
        
        self.model_provider = OllamaProvider(model_name)
        self.tool_executor = ToolExecutor(self.registry)
        self.agent = OneMinuteAgent(
            model_provider=self.model_provider,
            tool_executor=self.tool_executor,
            max_iterations=2,
            show_thinking=show_thinking
        )
    
    def chat(self, message: str) -> Dict[str, Any]:
        """
        Main chat interface for frontends.
        
        Args:
            message: User message (typically from 911 operator)
            
        Returns:
            Dict with response, tools used, and metadata
        """
        response = self.agent.chat(message)
        
        return {
            "response": response.content,
            "tools_executed": response.tools_executed,
            "metadata": response.metadata or {},
            "success": True
        }
    
    def clear_conversation(self) -> Dict[str, str]:
        """Clear conversation history"""
        self.agent.clear_conversation()
        return {"status": "conversation_cleared"}
    
    def get_conversation_history(self) -> Dict[str, Any]:
        """Get conversation history for frontend display"""
        history = self.agent.get_conversation_history()
        return {
            "messages": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "metadata": msg.metadata
                }
                for msg in history
            ],
            "count": len(history)
        }
    
    def get_available_tools(self) -> Dict[str, Any]:
        """Get available emergency tools"""
        return {
            "tools": self.tool_executor.get_available_tools(),
            "domains": self.registry.get_tool_domains()
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Health check for the API"""
        try:
            test_response = self.agent.should_use_reasoning_loop("test")
            return {
                "status": "healthy",
                "model": self.model_provider.model_name,
                "tools_count": len(self.registry.tools),
                "test_passed": isinstance(test_response, bool)
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e)
            }

def create_emergency_agent(model_name: str = "gemma3n:e2b", show_thinking: bool = False) -> OneMinuteAgentAPI:
    """
    Quick factory function to create an one-minute agent.
    Perfect for frontend integration.
    """
    return OneMinuteAgentAPI(model_name=model_name, show_thinking=show_thinking)

def create_custom_emergency_agent(
    model_name: str = "gemma3n:e2b",
    additional_tools: Optional[Dict[str, Any]] = None,
    show_thinking: bool = False
) -> OneMinuteAgentAPI:
    """
    Create an one-minute agent with custom tools.
    
    Args:
        model_name: Ollama model name
        additional_tools: Dict of additional tools to register
        show_thinking: Whether to show the agent's thinking process
        
    Returns:
        Configured OneMinuteAgentAPI instance
    """
    api = OneMinuteAgentAPI(model_name=model_name, use_custom_registry=True, show_thinking=show_thinking)
    
    if additional_tools:
        for name, tool_config in additional_tools.items():
            api.registry.register_function(
                name=name,
                func=tool_config["func"],
                description=tool_config["description"],
                parameters=tool_config.get("parameters", {}),
                domain=tool_config.get("domain", "custom")
            )
    
    return api