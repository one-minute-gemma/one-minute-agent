"""
Base LLM handler with shared functionality for conversation management,
tool execution, and crisis response logic.
"""
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any, Optional
from ..tools.emergency_tools import get_available_tools, execute_tool

logger = logging.getLogger(__name__)

class LLMHandler(ABC):
    """
    Abstract base class for LLM handlers with function calling capability.
    """
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.messages: List[Dict[str, str]] = []
        self.available_tools = get_available_tools()
        logger.info(f"{self.__class__.__name__} initialized with model: {model_name}")

    def handle_message(self, user_input: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Process a user message and return response with any executed tools.
        This is the main public interface for all handlers.
        Returns: (assistant_response, executed_tools)
        """
        # Add user message to history
        self.messages.append({"role": "user", "content": user_input})
        
        try:
            # Build system prompt with tools
            system_prompt = self._build_system_prompt()
            
            # Call the model (implementation-specific)
            response_content = self._call_model(system_prompt)
            logger.info(f"Raw model response: {response_content}")
            
            # Process the structured response
            assistant_response, executed_tools = self._process_model_response(response_content)
            
            # Add assistant response to history
            self.messages.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response, executed_tools
            
        except Exception as e:
            error_msg = f"Error communicating with model: {e}"
            logger.error(error_msg, exc_info=True)
            
            # Remove the last user message on error so they can retry
            if self.messages and self.messages[-1]["role"] == "user":
                self.messages.pop()
            
            return error_msg, []

    @abstractmethod
    def _call_model(self, system_prompt: str) -> str:
        """
        Call the specific model implementation (Ollama, Gemini, etc.)
        This must be implemented by each handler subclass.
        Returns: Raw response content from the model
        """
        pass

    @abstractmethod
    def _prepare_messages_for_model(self, system_prompt: str) -> Any:
        """
        Format messages for the specific model's expected format.
        Different APIs have different message structures.
        """
        pass

    def _build_system_prompt(self) -> str:
        """Build system prompt with available tools (shared across all handlers)"""
        tools_json = json.dumps(self.available_tools, indent=2)
        return f"""You are a helpful crisis response assistant. Analyze user messages for emergency situations and respond appropriately.

Available emergency tools:
{tools_json}

Instructions:
- If you detect a crisis situation (like "I've fallen", "help me", "emergency", "can't breathe", etc.), use the available tools
- Always respond with valid JSON in this exact format:

For crisis situations:
{{
    "crisis_detected": true,
    "crisis_type": "fall" | "medical" | "panic" | "other",
    "confidence": 0.8,
    "tools_to_call": [
        {{"tool": "call_emergency_contact", "args": {{"contact_type": "primary"}}}},
        {{"tool": "log_incident", "args": {{"incident_type": "fall", "severity": "medium"}}}}
    ],
    "response": "I've detected you may have fallen! I'm calling your emergency contact and logging this incident. Help is on the way!"
}}

For normal conversations:
{{
    "crisis_detected": false,
    "response": "Your normal helpful response to the user"
}}

IMPORTANT: Always respond with valid JSON. Do not include any text outside the JSON structure."""

    def _process_model_response(self, response_content: str) -> Tuple[str, List[Dict[str, Any]]]:
        """Process the model's JSON response and execute any tools (shared logic)"""
        try:
            # Parse the JSON response
            parsed = json.loads(response_content.strip())
            executed_tools = []
            
            # Check if crisis detected and execute tools
            if parsed.get("crisis_detected", False):
                print("🚨 Crisis detected! Executing emergency tools...")
                
                for tool_call in parsed.get("tools_to_call", []):
                    tool_name = tool_call.get("tool")
                    tool_args = tool_call.get("args", {})
                    
                    print(f"🔧 Executing tool: {tool_name}")
                    result = execute_tool(tool_name, tool_args)
                    
                    executed_tools.append({
                        "tool": tool_name,
                        "args": tool_args,
                        "result": result
                    })
            
            response_text = parsed.get("response", "I'm here to help.")
            return response_text, executed_tools
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Raw response: {response_content}")
            return "I'm having trouble processing your request. Are you okay?", []

    def clear_history(self):
        """Clear the conversation history"""
        self.messages = []
        logger.info("Conversation history cleared")

    def get_conversation_length(self) -> int:
        """Get the number of messages in the conversation"""
        return len(self.messages)

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get a copy of the conversation history"""
        return self.messages.copy()

    def add_system_message(self, content: str):
        """Add a system message to the conversation"""
        self.messages.append({"role": "system", "content": content})

    def set_tools(self, tools: Dict[str, Dict]):
        """Override the available tools (useful for testing or customization)"""
        self.available_tools = tools
        logger.info(f"Tools updated: {list(tools.keys())}") 