"""
Generic tool registry system for managing and executing tools.
Supports different tool domains (emergency, general, etc.) and providers.
"""
from typing import Dict, Any, Callable, Optional, List
from dataclasses import dataclass
from abc import ABC, abstractmethod
import asyncio
import inspect
import logging

logger = logging.getLogger(__name__)

@dataclass
class ToolDefinition:
    """Tool definition with metadata"""
    name: str
    description: str
    parameters: Dict[str, Any]
    func: Callable
    domain: str = "general"
    async_func: bool = False

class ToolProvider(ABC):
    """Abstract base for tool providers"""
    
    @abstractmethod
    def get_tools(self) -> List[ToolDefinition]:
        """Return list of tools provided by this provider"""
        pass

class ToolRegistry:
    """
    Central registry for managing tools across different domains.
    Supports both sync and async tools, multiple providers.
    """
    
    def __init__(self):
        self.tools: Dict[str, ToolDefinition] = {}
        self.providers: List[ToolProvider] = []
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
    
    def register_provider(self, provider: ToolProvider) -> None:
        """Register a tool provider"""
        self.providers.append(provider)
        
        for tool in provider.get_tools():
            self.register_tool(tool)
    
    def register_tool(self, tool: ToolDefinition) -> None:
        """Register a single tool"""
        if tool.name in self.tools:
            self.logger.warning(f"Tool {tool.name} already registered, overwriting")
        
        self.tools[tool.name] = tool
        self.logger.debug(f"Registered tool: {tool.name} (domain: {tool.domain})")
    
    def register_function(
        self, 
        name: str, 
        func: Callable, 
        description: str,
        parameters: Optional[Dict[str, Any]] = None,
        domain: str = "general"
    ) -> None:
        """Register a function directly as a tool"""
        is_async = inspect.iscoroutinefunction(func)
        
        tool = ToolDefinition(
            name=name,
            description=description,
            parameters=parameters or {},
            func=func,
            domain=domain,
            async_func=is_async
        )
        
        self.register_tool(tool)
    
    def get_available_tools(self, domain: Optional[str] = None) -> Dict[str, Dict]:
        """Get tools formatted for LLM consumption"""
        filtered_tools = self.tools
        
        if domain:
            filtered_tools = {
                name: tool for name, tool in self.tools.items() 
                if tool.domain == domain
            }
        
        return {
            name: {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters,
                "domain": tool.domain
            }
            for name, tool in filtered_tools.items()
        }
    
    def has_tool(self, name: str) -> bool:
        """Check if tool exists"""
        return name in self.tools
    
    def get_tool_domains(self) -> List[str]:
        """Get all available tool domains"""
        return list(set(tool.domain for tool in self.tools.values()))

class ToolExecutor:
    """
    Executes tools from the registry.
    Handles both sync and async tools properly.
    """
    
    def __init__(self, registry: ToolRegistry):
        self.registry = registry
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
    
    def execute(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool and return result"""
        if not self.registry.has_tool(tool_name):
            return {
                "status": "error",
                "message": f"Tool '{tool_name}' not found"
            }
        
        tool = self.registry.tools[tool_name]
        
        try:
            self.logger.debug(f"Executing tool: {tool_name} with args: {args}")
            
            if tool.async_func:
                # Handle async function
                result = asyncio.run(tool.func(**args))
            else:
                # Handle sync function
                result = tool.func(**args)
            
            return {
                "status": "success",
                "data": result,
                "tool": tool_name
            }
            
        except Exception as e:
            self.logger.error(f"Tool execution failed: {tool_name} - {e}", exc_info=True)
            return {
                "status": "error",
                "message": f"Tool execution failed: {str(e)}",
                "tool": tool_name
            }
    
    def get_available_tools(self) -> Dict[str, Dict]:
        """Get available tools (implements ToolExecutor protocol)"""
        return self.registry.get_available_tools()
    
    def execute_batch(self, tool_calls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Execute multiple tools in sequence"""
        results = []
        
        for call in tool_calls:
            tool_name = call.get("tool")
            args = call.get("args", {})
            
            result = self.execute(tool_name, args)
            results.append({
                "tool": tool_name,
                "args": args,
                "result": result
            })
        
        return results

# Global registry instance - can be used across the application
default_registry = ToolRegistry() 