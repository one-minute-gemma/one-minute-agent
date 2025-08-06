"""
Mock provider for demo purposes when Ollama is not available.
"""
import json
import random
from typing import List
from ..base.agent import ModelProvider, Message

class MockProvider(ModelProvider):
    """Mock implementation for demo purposes"""
    
    def __init__(self, model_name: str = "mock-demo"):
        self.model_name = model_name
        self.call_count = 0
        
        self.victim_responses = [
            "I understand you're in an emergency situation. Help is on the way. Can you tell me if you're in a safe location right now?",
            "Thank you for that information. Emergency responders are approximately 3-4 minutes away. Please stay with me.",
            "You're doing great. Keep talking to me while we wait for help to arrive.",
            "I've updated the emergency team with your information. They should be there very soon.",
            "Please stay calm. Can you tell me if anyone else is with you right now?",
            "That's very helpful information. I'm relaying this to the responders right now.",
            "You're being very brave. Help will be there in just a few minutes.",
        ]
        
        self.operator_responses = [
            "Unit 23 dispatched to location. ETA 4 minutes.",
            "Fire department and paramedics en route. Emergency confirmed at location.", 
            "Additional units being dispatched. Maintaining communication with victim.",
            "Responders are 2 minutes out. Preparing for arrival.",
            "Emergency team briefed on situation. Standing by for updates.",
            "All units converging on location. ETA reduced to 90 seconds.",
        ]

    def chat(self, messages: List[Message], system_prompt: str) -> str:
        """Return mock responses"""
        self.call_count += 1
        
        # Determine agent type from system prompt
        if "victim" in system_prompt.lower() or "assistant" in system_prompt.lower():
            responses = self.victim_responses
        else:
            responses = self.operator_responses
        
        # Get a response based on call count
        response_text = responses[(self.call_count - 1) % len(responses)]
        
        # Return in expected JSON format
        return json.dumps({
            "thought": "This is an emergency response situation requiring immediate attention.",
            "action": "None",
            "actionInput": {},
            "response": response_text
        }) 