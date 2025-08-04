"""
Generic base agent class following TypeScript-like patterns.
Framework-agnostic and easily pluggable into frontends.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional, Tuple, Protocol
from dataclasses import dataclass
import json
import logging

logger = logging.getLogger(__name__)

@dataclass
class AgentResponse:
    """Standardized agent response format"""
    content: str
    tools_executed: List[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class Message:
    """Message format for conversations"""
    role: str  # "user", "assistant", "system"
    content: str
    metadata: Optional[Dict[str, Any]] = None

class ToolExecutor(Protocol):
    """Protocol for tool execution - allows different implementations"""
    def execute(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        ...
    
    def get_available_tools(self) -> Dict[str, Dict]:
        ...

class ModelProvider(Protocol):
    """Protocol for different LLM providers (Ollama, OpenAI, etc.)"""
    def chat(self, messages: List[Message], system_prompt: str) -> str:
        ...

class BaseAgent(ABC):
    """
    Generic agent base class that can be extended for specific use cases.
    Handles conversation management, reasoning loops, and tool coordination.
    """
    
    def __init__(
        self, 
        model_provider: ModelProvider,
        tool_executor: Optional[ToolExecutor] = None,
        max_iterations: int = 3,
        show_thinking: bool = False,
        always_use_reasoning: bool = True
    ):
        self.model_provider = model_provider
        self.tool_executor = tool_executor
        self.max_iterations = max_iterations
        self.messages: List[Message] = []
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self.show_thinking = show_thinking
        self.always_use_reasoning = always_use_reasoning

    # Public API

    def chat(self, user_input: str) -> AgentResponse:
        """
        Main chat interface - handles a user message and returns response.
        This is the primary method frontends should call.
        """
        try:
            self.messages.append(Message(role="user", content=user_input))
            
            if self.should_use_reasoning_loop(user_input):
                return self._reasoning_loop()
            else:
                return self._simple_response()
                
        except Exception as e:
            self.logger.error(f"Error in chat: {e}", exc_info=True)
            # Remove failed user message
            if self.messages and self.messages[-1].role == "user":
                self.messages.pop()
            
            return AgentResponse(
                content="I encountered an error processing your request. Please try again.",
                tools_executed=[],
                metadata={"error": str(e)}
            )
    
    def clear_conversation(self) -> None:
        """Clear conversation history"""
        self.messages = []
    
    def get_conversation_history(self) -> List[Message]:
        """Get conversation history (useful for frontends)"""
        return self.messages.copy()
    
    # Abstract methods - subclasses implement specific behavior
    
    @abstractmethod
    def should_use_reasoning_loop(self, user_input: str) -> bool:
        """Determine if this input requires multi-step reasoning"""
        pass
    
    @abstractmethod
    def build_system_prompt(self) -> str:
        """Build the system prompt for this agent type"""
        pass
    
    @abstractmethod
    def parse_reasoning_response(self, response: str) -> Optional[Dict[str, Any]]:
        """Parse a reasoning step response from the model"""
        pass
    
    @abstractmethod
    def parse_final_response(self, response: str) -> str:
        """Parse the final response from the model"""
        pass
    
    # Protected methods - for subclass use
    
    def _reasoning_loop(self) -> AgentResponse:
        """Execute multi-step reasoning with tool calls"""
        executed_tools = []
        called_tools = set()
        
        system_prompt = self.build_system_prompt()
        
        for iteration in range(self.max_iterations):
            if self.show_thinking:
                self.logger.info(f"🧠 Reasoning iteration {iteration + 1}/{self.max_iterations}")
            
            response = self.model_provider.chat(self.messages, system_prompt)
            
            parsed = self.parse_reasoning_response(response)
            if not parsed:
                if self.show_thinking:
                    self.logger.info("❌ Could not parse response, getting final answer")
                break
            
            if self.show_thinking:
                thought = parsed.get("thought", "")
                action = parsed.get("action", "None")
                self.logger.info(f"💭 Thought: {thought}")
                self.logger.info(f"🎯 Action: {action}")
            
            action = parsed.get("action")
            
            if (not action or action.lower() == "none"):
                
                if self.show_thinking: 
                    self.logger.info("✅ Agent ready to provide final answer")
                break
            
            if (self.tool_executor and 
                action in self.tool_executor.get_available_tools() and 
                action not in called_tools):
                
                if self.show_thinking:
                    self.logger.info(f"🔧 Executing tool: {action}")
                
                tool_result = self.tool_executor.execute(
                    action, 
                    parsed.get("actionInput", {})
                )
                
                executed_tools.append({
                    "tool": action,
                    "args": parsed.get("actionInput", {}),
                    "result": tool_result
                })
                
                called_tools.add(action)
                
                self.messages.append(Message(
                    role="system", 
                    content=f"Tool result: {json.dumps(tool_result)}"
                ))
            else:
                if self.show_thinking:
                    if action in called_tools:
                        self.logger.info(f"⚠️ Tool {action} already called, proceeding to final answer")
                    else:
                        self.logger.info(f"❌ Unknown tool {action}, proceeding to final answer")
                break
        
        if self.show_thinking:
            self.logger.info("🎯 Getting final answer from agent")
        
        final_response = self._get_final_answer()
        
        self.messages.append(Message(role="assistant", content=final_response))
        
        return AgentResponse(
            content=final_response,
            tools_executed=executed_tools,
            metadata={
                "thinking_iterations": iteration + 1, 
                "tools_used": len(executed_tools)
            }
        )
    
    def _simple_response(self) -> AgentResponse:
        """Get a simple response without reasoning loop"""
        if self.show_thinking:
            self.logger.info("Using simple response mode (no reasoning loop)")
        
        system_prompt = self.build_system_prompt()
        response = self.model_provider.chat(self.messages, system_prompt)
        final_response = self.parse_final_response(response)
        
        if self.show_thinking:
            self.logger.info(f"Simple response generated: {final_response[:100]}...")
        
        self.messages.append(Message(role="assistant", content=final_response))
        
        return AgentResponse(
            content=final_response,
            tools_executed=[],
            metadata={"type": "simple"}
        )
    
    def _get_final_answer(self) -> str:
        """Get the final answer from the model"""
        final_prompt = """FINAL ANSWER MODE: Based on the conversation context and actual data gathered from tool results, provide your final response clearly and decisively.

        CRITICAL RULES:

        * ONLY provide verified information explicitly obtained from previous tool results.
        * NEVER assume or invent data.
        * Clearly indicate if essential data (e.g., location) is missing.
        * Provide an immediate, actionable response relevant to the emergency.
        * Avoid placeholders or requests for further action or tool usage.

        Answer strictly in this format:
        {
        "answer": "Your complete and precise final response here"
        }

        Examples of BAD responses:

        * {
        "answer": "I need additional tools or information to respond."
        }
        * {
        "answer": "More data must be collected before I can answer."
        }

        Example of a GOOD response:

        * {
        "answer": "The person is experiencing severe chest pain. Their location is 123 Main Street. Immediate medical assistance is required."
        }

        Provide your final response now:"""
        
        response = self.model_provider.chat(self.messages, final_prompt)
        final_answer = self.parse_final_response(response)
        
        if self.show_thinking:
            self.logger.info(f"Final answer: {final_answer}")
        
        return final_answer