"""
VictimAssistantAgent - provides real-time help directly to emergency victims.
Extends BaseAgent with victim-focused guidance and first aid instructions.
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional
from nagents import BaseAgent

class VictimAssistantAgent(BaseAgent):
    """
    Emergency victim assistance agent that provides real-time help directly to victims.
    Features calming communication, first aid guidance, and situation assessment.
    """
    
    def __init__(self, model_provider, tool_executor, max_iterations: int = 3, show_thinking: bool = False, always_use_reasoning: bool = True):
        super().__init__(model_provider, tool_executor, max_iterations, show_thinking, always_use_reasoning)
        self.prompt_template = self._load_prompt_template()
    
    def _load_prompt_template(self) -> str:
        """Load the victim assistance prompt template"""
        prompt_path = Path(__file__).parent / "prompts" / "prompt.md"
        try:
            with open(prompt_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            return self._get_default_victim_assistance_prompt()
    
    def should_use_reasoning_loop(self, user_input: str) -> bool:
        """
        Victim assistant uses reasoning for medical emergencies, injury assessment, and guidance requests.
        """
        if self.always_use_reasoning:
            return True

        user_input_lower = user_input.lower()
        
        assistance_triggers = [
            "help", "pain", "hurt", "bleeding", "breathe", "breathing",
            "chest", "heart", "dizzy", "unconscious", "fell", "injury",
            "burn", "cut", "broken", "sprain", "choke", "choking",
            "allergic", "poison", "overdose", "seizure", "stroke",
            "what do i do", "how do i", "should i", "first aid",
            "emergency", "911", "ambulance", "hospital"
        ]
        
        return any(trigger in user_input_lower for trigger in assistance_triggers)
    
    def build_system_prompt(self) -> str:
        """Build victim assistance system prompt with available tools"""
        available_tools = {}
        if self.tool_executor:
            available_tools = self.tool_executor.get_available_tools()
        
        tools_json = json.dumps(available_tools, indent=2)
        
        return f"""{self.prompt_template}

            ## AVAILABLE ASSISTANCE TOOLS:
            {tools_json}

            Available tools: {', '.join(available_tools.keys()) if available_tools else 'None'}

            Remember: You are helping someone who may be scared, injured, or in crisis. Be calm, clear, and supportive.
            """
    
    def parse_reasoning_response(self, response: str) -> Optional[Dict[str, Any]]:
        """Parse victim assistance reasoning response"""
        try:
            parsed = json.loads(response.strip())
            
            if "thought" not in parsed:
                parsed["thought"] = "Assessing situation to provide appropriate assistance..."
            if "action" not in parsed:
                parsed["action"] = "None"
            if "actionInput" not in parsed:
                parsed["actionInput"] = {}
                
            return parsed
            
        except json.JSONDecodeError:
            return self._parse_malformed_reasoning(response)
    
    def _parse_malformed_reasoning(self, response: str) -> Optional[Dict[str, Any]]:
        """Parse malformed reasoning response for victim assistance"""
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
        """Parse final victim assistance response and convert to direct address"""
        try:
            parsed = json.loads(response.strip())
            answer = parsed.get("answer", response.strip())
            return self._convert_to_direct_address(answer)
        except json.JSONDecodeError:
            return self._convert_to_direct_address(response.strip())
            
    def _convert_to_direct_address(self, text: str) -> str:
        """Convert third-person instructions to direct second-person address"""
        # Common third-person phrases to replace
        replacements = {
            "the person should": "you should",
            "the person needs to": "you need to",
            "the person must": "you must",
            "the person can": "you can",
            "the person has": "you have",
            "the person is": "you are",
            "the patient should": "you should",
            "the patient needs to": "you need to",
            "the patient must": "you must",
            "the patient can": "you can",
            "the patient has": "you have",
            "the patient is": "you are",
            "have the person": "",
            "tell the person to": "",
            "ask the person to": "",
            "help the person": "",
            "assist the person to": "",
            "the person": "you",
            "the patient": "you",
            "their": "your",
            "they": "you",
            "them": "you"
        }
        
        result = text
        for old, new in replacements.items():
            # Case insensitive replacement
            result = result.replace(old, new)
            result = result.replace(old.capitalize(), new.capitalize())
        
        return result
    
    def _get_default_victim_assistance_prompt(self) -> str:
        """Default victim assistance prompt if file not found"""
        return """# Emergency Victim Assistance Agent

            ## ROLE:
            You are an AI emergency assistant providing DIRECT help to someone experiencing an emergency. You communicate directly with the victim to provide guidance, comfort, and life-saving instructions.

            ## CRITICAL PERSPECTIVE:
            - You are speaking DIRECTLY to the person in need
            - Use "you" when addressing them, not "the person" or "they"
            - Be calm, reassuring, and clear in your instructions
            - Your primary goal is to keep them safe until help arrives

            ## CRITICAL BEHAVIOR:
            When someone asks for help or describes an emergency:
            1. Assess their immediate situation using available tools
            2. Provide clear, step-by-step guidance
            3. Keep them calm and focused
            4. Give practical first aid instructions when appropriate
            5. Monitor their condition and adjust advice accordingly

            ## EXAMPLE RESPONSES:
            ✅ CORRECT: "Take a deep breath. I'm here to help you."
            ✅ CORRECT: "Apply pressure to the wound with a clean cloth."
            ✅ CORRECT: "Stay on the line with me. You're doing great."

            ❌ WRONG: "The person should apply pressure to the wound"
            ❌ WRONG: "Tell them to stay calm"

            ## REASONING FORMAT:
            For information gathering, respond with:
            {
            "thought": "I need to assess [specific aspect] to provide the right guidance",
            "action": "tool_name",
            "actionInput": {}
            }

            When you have enough information, respond with:
            {
            "thought": "I have sufficient information to guide them through this situation",
            "action": "None",
            "actionInput": {}
            }

            For final responses, respond with:
            {
            "answer": "Clear, supportive guidance and instructions for the victim"
            }

            ## ASSISTANCE PRIORITIES:
            1. Immediate life threats (breathing, consciousness, severe bleeding)
            2. Pain management and comfort measures
            3. First aid instructions and safety measures
            4. Emotional support and reassurance
            5. Preparation for emergency responders

            ## COMMUNICATION STYLE:
            - Speak directly to the victim ("you", not "they")
            - Use simple, clear language
            - Be calm and reassuring
            - Give one instruction at a time
            - Ask for confirmation they understand
            - Provide encouragement and support

            ## IMPORTANT:
            - After gathering 1-2 pieces of information, provide guidance
            - Don't overwhelm them with too many questions
            - Focus on immediate, actionable steps they can take
            - Keep them engaged and responsive
            - Always reassure them that help is coming""" 