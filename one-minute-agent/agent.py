"""
OneMinuteAgent Agent - specialized agent for 911 emergency response with operators.
Extends BaseAgent with emergency-specific reasoning and behavior.
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional
from nagents import BaseAgent

class OneMinuteAgent(BaseAgent):
    """
    Emergency response agent optimized for 911 operator communication.
    Features fast decision-making, emergency tool prioritization, and crisis detection.
    """
    
    def __init__(self, model_provider, tool_executor, max_iterations: int = 2, show_thinking: bool = False, always_use_reasoning: bool = True):
        super().__init__(model_provider, tool_executor, max_iterations, show_thinking, always_use_reasoning)
        self.prompt_template = self._load_prompt_template()
    
    def _load_prompt_template(self) -> str:
        """Load the emergency agent prompt template"""
        prompt_path = Path(__file__).parent / "prompts" / "prompt.md"
        try:
            with open(prompt_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            return self._get_default_emergency_prompt()
    
    def should_use_reasoning_loop(self, user_input: str) -> bool:
        """
        Emergency agent uses reasoning loop for any operator interaction that might need information gathering.
        Emergency agent uses reasoning loop for any operator interaction that might need information gathering.
        """

        if self.always_use_reasoning:
            return True

        user_input_lower = user_input.lower()
        
        # Always use reasoning for emergency-related queries
        emergency_triggers = [
            "what's your emergency",
            "emergency",
            "location", 
            "condition",
            "what happened",
            "medical",
            "symptoms",
            "vitals",
            "health",
            "injured"
        ]
        
        greeting_triggers = [
            "hello",
            "hi",
            "hey",
            "good morning",
            "good afternoon", 
            "good evening",
            "this is 911"
        ]
        
        return (any(trigger in user_input_lower for trigger in emergency_triggers) or
                any(trigger in user_input_lower for trigger in greeting_triggers))
    
    def build_system_prompt(self) -> str:
        """Build emergency-specific system prompt with available tools"""
        available_tools = {}
        if self.tool_executor:
            available_tools = self.tool_executor.get_available_tools()
        
        tools_json = json.dumps(available_tools, indent=2)
        
        return f"""{self.prompt_template}

            ## AVAILABLE EMERGENCY TOOLS:
            {tools_json}

            Available tools: {', '.join(available_tools.keys()) if available_tools else 'None'}

            Remember: You are communicating with a 911 operator. Be decisive, clear, and prioritize life-saving information.
            """
    
    def parse_reasoning_response(self, response: str) -> Optional[Dict[str, Any]]:
        """Parse emergency reasoning response with improved error handling"""
        try:
            parsed = json.loads(response.strip())
            
            if "thought" not in parsed:
                parsed["thought"] = "Analyzing emergency situation..."
            if "action" not in parsed:
                parsed["action"] = "None"
            if "actionInput" not in parsed:
                parsed["actionInput"] = {}
                
            return parsed
            
        except json.JSONDecodeError:
            return self._parse_malformed_reasoning(response)
    
    def _parse_malformed_reasoning(self, response: str) -> Optional[Dict[str, Any]]:
        """Parse malformed reasoning response"""
        lines = response.strip().split('\n')
        result = {
            "thought": "",
            "action": "None",
            "actionInput": {}
        }
        
        for line in lines:
            line = line.strip()
            if any(key in line.lower() for key in ['thought:', '"thought":']):
                result['thought'] = self._extract_value_from_line(line, 'thought')
            elif any(key in line.lower() for key in ['action:', '"action":']):
                result['action'] = self._extract_value_from_line(line, 'action')
            elif any(key in line.lower() for key in ['actioninput:', '"actioninput":']):
                try:
                    input_str = self._extract_value_from_line(line, 'actioninput')
                    result['actionInput'] = json.loads(input_str) if input_str and input_str != 'null' else {}
                except:
                    result['actionInput'] = {}
        
        return result if result['thought'] or result['action'] != "None" else None
    
    def _extract_value_from_line(self, line: str, key: str) -> str:
        """Extract value from a line like 'thought: "some value"'"""
        try:
            key_variants = [f'"{key}":', f'{key}:']
            for variant in key_variants:
                if variant in line.lower():
                    value = line.lower().split(variant, 1)[1]
                    break
            else:
                return ""
            
            value = value.strip().rstrip(',')
            
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            
            return value
        except:
            return ""
    
    def parse_final_response(self, response: str) -> str:
        """Parse final emergency response"""
        try:
            parsed = json.loads(response.strip())
            if "answer" in parsed:
                return parsed["answer"]
            elif "thought" in parsed:
                return parsed["thought"]
            else:
                return response.strip()
        except json.JSONDecodeError:
            return response.strip()
    
    def _get_default_emergency_prompt(self) -> str:
        """Default emergency prompt if file not found"""

        with open("prompts/prompt.md", "r") as f:
            prompt = f.read()

        return prompt