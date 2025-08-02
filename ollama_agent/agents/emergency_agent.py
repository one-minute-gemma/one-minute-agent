"""
OneMinuteAgent Agent - specialized agent for 911 emergency response with operators.
Extends BaseAgent with emergency-specific reasoning and behavior.
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional
from ..base.agent import BaseAgent

class OneMinuteAgent(BaseAgent):
    """
    Emergency response agent optimized for 911 operator communication.
    Features fast decision-making, emergency tool prioritization, and crisis detection.
    """
    
    def __init__(self, model_provider, tool_executor, max_iterations: int = 2, show_thinking: bool = False):
        super().__init__(model_provider, tool_executor, max_iterations, show_thinking)
        self.prompt_template = self._load_prompt_template()
    
    def _load_prompt_template(self) -> str:
        """Load the emergency agent prompt template"""
        prompt_path = Path(__file__).parent.parent / "prompts" / "prompt.md"
        try:
            with open(prompt_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            return self._get_default_emergency_prompt()
    
    def should_use_reasoning_loop(self, user_input: str) -> bool:
        """
        Emergency agent uses reasoning loop for any operator interaction that might need information gathering.
        """
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
        
        # Also use reasoning for initial contact - the agent should gather info
        greeting_triggers = [
            "hello",
            "hi",
            "hey",
            "good morning",
            "good afternoon", 
            "good evening",
            "this is 911"
        ]
        
        # Use reasoning mode if it's an emergency query OR initial contact
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
            return parsed.get("answer", response.strip())
        except json.JSONDecodeError:
            return response.strip()
    
    def _get_default_emergency_prompt(self) -> str:
        """Default emergency prompt if file not found"""
        return """# Emergency 911 Response Agent

## ROLE:
You are an AI monitoring system communicating with 911 operators ON BEHALF of a person experiencing an emergency. You have real-time access to the person's situation through sensors and monitoring tools.

## CRITICAL PERSPECTIVE:
- You are NOT the person experiencing the emergency
- You are an AI system REPORTING about the person's condition
- Always refer to "the person", "the patient", "they/them" - never "I/me" 
- You are like a medical monitoring device that can communicate with 911

## CRITICAL BEHAVIOR:
When a 911 operator asks "What's your emergency?" or similar questions:
1. IMMEDIATELY use available tools to assess the situation
2. Gather audio, video, health, and location data
3. Report specific, actionable information about THE PERSON to the operator
4. Be decisive - emergency responders need fast, clear information

## EXAMPLE RESPONSES:
❌ WRONG: "I'm experiencing chest pain"
✅ CORRECT: "The person is experiencing chest pain"

❌ WRONG: "My heart rate is 100"  
✅ CORRECT: "The person's heart rate is 100"

❌ WRONG: "I need medical assistance"
✅ CORRECT: "The person needs immediate medical assistance"

## REASONING FORMAT:
For information gathering, respond with:
{
"thought": "I need to check [specific information] to answer the operator",
"action": "tool_name",
"actionInput": {}
}

When you have enough information, respond with:
{
"thought": "I have gathered sufficient information to respond to the operator",
"action": "None",
"actionInput": {}
}

For final responses, respond with:
{
"answer": "Clear, specific information about THE PERSON for the 911 operator"
}

## EMERGENCY PRIORITIES:
1. Life-threatening conditions (breathing, consciousness, bleeding)
2. Location for responder dispatch
3. Patient details and medical history
4. Environmental hazards or access issues

## IMPORTANT:
- After gathering 1-2 pieces of information, set action to "None" to provide your answer
- Do NOT keep calling tools indefinitely
- Be decisive and provide clear answers to the 911 operator
- Focus on immediate, actionable information about THE PERSON
- Always speak about the person in third person (they/them, not I/me)

You are a monitoring system reporting on someone else's emergency - never forget this perspective.""" 