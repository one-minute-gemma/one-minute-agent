import json
import asyncio
from typing import Dict, Any, List, Tuple, Optional
from .src.handlers.llm_handler import LLMHandler
from pathlib import Path
import ollama

from . import tools

class OMHandler(LLMHandler):
    """
    Emergency-optimized agentic handler with iterative reasoning and tool execution.
    Implements a ReAct-style (Reasoning + Acting) pattern optimized for emergency response.
    
    Key features:
    - One tool per iteration for methodical step-by-step processing
    - Maximum 2 iterations for emergency speed
    - Prevents redundant tool calls
    - Prioritizes decisive action over thoroughness
    """
    
    def __init__(self, model_name: str = "gemma3n:e2b"):
        # Initialize without calling super().__init__ to avoid loading emergency tools
        self.model_name = model_name
        self.messages: List[Dict[str, str]] = []
        self.available_tools = self._get_custom_tools()

    def _get_custom_tools(self) -> Dict[str, Dict]:
        """Define available tools from our tools.py module"""
        return {
            "get_health_metrics": {
                "name": "get_health_metrics",
                "description": "Returns the current health metrics of the user (heart_rate, blood_pressure, blood_oxygen)",
                "parameters": {}
            },
            "get_user_location": {
                "name": "get_user_location", 
                "description": "Returns the current location of the user (latitude, longitude)",
                "parameters": {}
            },
            "get_audio_input": {
                "name": "get_audio_input",
                "description": "Returns simulated audio input from the user indicating emergency situations",
                "parameters": {}
            },
            "get_video_input": {
                "name": "get_video_input",
                "description": "Returns a sample emergency image for multimodal analysis",
                "parameters": {}
            },
            "get_user_details": {
                "name": "get_user_details",
                "description": "Returns detailed personal and medical information about the user",
                "parameters": {}
            }
        }

    def handle_message(self, user_input: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Enhanced agentic message handling with iterative reasoning.
        Implements a ReAct-style loop: Thought -> Action -> Observation -> Repeat
        ONE TOOL PER ITERATION for methodical processing.
        EMERGENCY-OPTIMIZED: Fast, decisive, no redundant calls.
        """
        # Add user message to history
        self.messages.append({"role": "user", "content": user_input})
        
        try:
            executed_tools = []
            called_tools = set()  # Track which tools we've already called
            max_iterations = 2  # Reduced for emergency speed
            
            print("\n🧠 **Agent Starting Reasoning Process...**")
            print("-" * 50)
            
            # Initial response from the model
            system_prompt = self._build_system_prompt()
            reply = self._call_model(system_prompt)
            
            # Iterative reasoning loop - ONE TOOL PER ITERATION
            for iteration in range(max_iterations):
                print(f"\n🧠 Reasoning iteration {iteration + 1}")
                
                # Parse the model's response
                parsed_response = self._parse_reasoning_response(reply)
                
                if not parsed_response:
                    print("❌ Could not parse response, ending reasoning")
                    break
                    
                thought = parsed_response.get("thought", "")
                action = parsed_response.get("action", "")
                action_input = parsed_response.get("actionInput", {})
                
                print(f"💭 Thought: {thought}")
                
                action = self._clean_action_name(action)
                
                if not action or action.lower() == "none":
                    print("\n🎯 Agent ready to provide final answer")
                    final_answer = self._get_final_answer()
                    final_parsed = self._parse_final_answer(final_answer)
                    final_text = final_parsed.get("answer", "I'm here to help.")
                    print("-" * 50)
                    return final_text, executed_tools
                
                if action not in self.available_tools:
                    print(f"❌ Unknown tool: {action}, ending reasoning")
                    break
                
                if action in called_tools:
                    print(f"⚠️ Tool {action} already called - being decisive with current info")
                    final_answer = self._get_final_answer()
                    final_parsed = self._parse_final_answer(final_answer)
                    final_text = final_parsed.get("answer", "Based on available information...")
                    print("-" * 50)
                    return final_text, executed_tools
                
                print(f"🔧 Executing action: {action}")
                tool_result = self._execute_custom_tool(action, action_input)
                called_tools.add(action)
                
                executed_tools.append({
                    "tool": action,
                    "args": action_input,
                    "result": tool_result
                })
                

                follow_up = self._create_emergency_followup(tool_result, called_tools)
                
                self.messages.append({"role": "system", "content": follow_up})
                reply = self._call_model(system_prompt)
            
            print(f"\n🎯 Max iterations reached, providing final answer")
            final_answer = self._get_final_answer()
            final_parsed = self._parse_final_answer(final_answer)
            final_text = final_parsed.get("answer", "I've reached my reasoning limit. Let me help you.")
            print("-" * 50)
            return final_text, executed_tools
            
        except Exception as e:
            error_msg = f"Error in agentic reasoning: {e}"
            print(error_msg)
            
            if self.messages and self.messages[-1]["role"] == "user":
                self.messages.pop()
            
            return error_msg, []

    def _clean_action_name(self, action: str) -> str:
        """Clean up action name to handle malformed responses"""
        if not action:
            return ""
        
        if "|" in action:
            action = action.split("|")[0]
        
        action = action.strip().strip('"').strip("'")
        
        return action

    def _parse_reasoning_response(self, response: str) -> Optional[Dict[str, Any]]:
        """Parse the model's reasoning response with improved error handling"""
        try:
            parsed = json.loads(response.strip())
            
            if "thought" not in parsed:
                parsed["thought"] = "Continuing analysis..."
            if "action" not in parsed:
                parsed["action"] = "None"
            if "actionInput" not in parsed:
                parsed["actionInput"] = {}
                
            return parsed
            
        except json.JSONDecodeError:
            lines = response.strip().split('\n')
            result = {
                "thought": "",
                "action": "None",
                "actionInput": {}
            }
            
            for line in lines:
                line = line.strip()
                if '"thought":' in line or 'thought:' in line:
                    result['thought'] = self._extract_value_from_line(line, 'thought')
                elif '"action":' in line or 'action:' in line:
                    result['action'] = self._extract_value_from_line(line, 'action')
                elif '"actionInput":' in line or 'actionInput:' in line:
                    try:
                        input_str = self._extract_value_from_line(line, 'actionInput')
                        result['actionInput'] = json.loads(input_str) if input_str and input_str != 'null' else {}
                    except:
                        result['actionInput'] = {}
            
            return result if result['thought'] or result['action'] != "None" else None

    def _extract_value_from_line(self, line: str, key: str) -> str:
        """Extract value from a line like 'thought: "some value"' or '"thought": "some value"' """
        try:
            if f'"{key}":' in line:
                value = line.split(f'"{key}":', 1)[1]
            elif f'{key}:' in line:
                value = line.split(f'{key}:', 1)[1]
            else:
                return ""
            
            value = value.strip().rstrip(',')
            
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            
            return value
        except:
            return ""

    def _parse_final_answer(self, response: str) -> Dict[str, str]:
        """Parse the final answer from the model"""
        try:
            return json.loads(response.strip())
        except json.JSONDecodeError:
            return {"answer": response.strip()}

    def _create_emergency_followup(self, tool_result: Dict[str, Any], called_tools: set) -> str:
        """Create a follow-up message for emergency situations, emphasizing decisive action."""
        observation_str = json.dumps(tool_result)
        
        return f"""
            Observation: {observation_str}

            EMERGENCY DECISION POINT: Can you answer the operator's question NOW with this information?

            Already called tools: {', '.join(called_tools)}
            DO NOT call the same tool again.

            If you have enough info to answer the operator's question → action: "None"
            If you need ONE more critical piece → call ONE different tool
            Remember: SPEED IS LIFE - be decisive, not perfect.
        """

    def _get_final_answer(self) -> str:
        """Get the final answer from the model"""
        final_prompt = """
        EMERGENCY RESPONSE: Answer the 911 operator's question NOW.

        Be direct, clear, and actionable. Emergency responders need fast information to save lives.
        Base your answer on the information you gathered - don't speculate or ask for more details.

        Examples of good emergency responses:
        - "Medical emergency: Person reports chest pain and says 'I'm dying'. Vitals show elevated heart rate."
        - "Person is coughing heavily, audio indicates respiratory distress."
        - "Location: 40.7128, -74.006 in New York City"
        - "Patient: John Doe, 30-year-old male, blood type A+, no known allergies."

        Respond with this exact JSON format:
        {
            "answer": "<your immediate, actionable response to the operator>"
        }
        """
        self.messages.append({"role": "system", "content": final_prompt})
        return self._call_model(self._build_system_prompt())

    def _call_model(self, system_prompt: str) -> str:
        """Call Ollama with the prepared messages"""
        messages = self._prepare_messages_for_model(system_prompt)
        
        response = ollama.chat(
            model=self.model_name,
            messages=messages,
            format="json"
        )
        
        return response['message']['content']

    def _prepare_messages_for_model(self, system_prompt: str) -> List[Dict[str, str]]:
        """Format messages for Ollama's expected format"""
        return [
            {"role": "system", "content": system_prompt}
        ] + self.messages
        
    def _build_system_prompt(self) -> str:
        """Build system prompt with available tools and reasoning instructions"""
        tools_json = json.dumps(self.available_tools, indent=2)
        
        prompt_path = Path(__file__).parent / "prompt.md"
        with open(prompt_path, "r") as file:
            base_prompt = file.read()
        
        enhanced_prompt = f"""{base_prompt}

            ## AVAILABLE TOOLS:
            {tools_json}

            Available tools: {', '.join(self.available_tools.keys())}
            """
        
        return enhanced_prompt

    def _execute_custom_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute one of our custom tools"""
        try:
            if tool_name == "get_health_metrics":
                result = asyncio.run(tools.get_health_metrics())
            elif tool_name == "get_user_location":
                result = asyncio.run(tools.get_user_location())
            elif tool_name == "get_audio_input":
                result = asyncio.run(tools.get_audio_input())
            elif tool_name == "get_video_input":
                result = asyncio.run(tools.get_video_input())
            elif tool_name == "get_user_details":
                result = asyncio.run(tools.get_user_details())
            else:
                return {"status": "error", "message": f"Unknown tool: {tool_name}"}
            
            return {"status": "success", "data": result}
            
        except Exception as e:
            return {"status": "error", "message": f"Tool execution failed: {str(e)}"}

