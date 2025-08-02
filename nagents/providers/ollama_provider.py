"""
Ollama model provider implementation.
Handles communication with Ollama models.
"""
import ollama
from typing import List
from ..base.agent import ModelProvider, Message

class OllamaProvider(ModelProvider):
    """Ollama implementation of ModelProvider protocol"""
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name

    def chat(self, messages: List[Message], system_prompt: str) -> str:
        """Chat with Ollama model"""
        ollama_messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        for msg in messages:
            ollama_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        response = ollama.chat(
            model=self.model_name,
            messages=ollama_messages,
            format="json"
        )
        
        return response['message']['content'] 