"""
Ollama model provider implementation.
Handles communication with Ollama models.
"""
import ollama
import json
import base64
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
        
        images = []
        
        for msg in messages:
            msg_images = self._extract_images_from_content(msg.content)
            if msg_images:
                images.extend(msg_images)
                print(f"🖼️ Found {len(msg_images)} images in message from {msg.role}")
            
            ollama_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        if images and ollama_messages:
            for i in reversed(range(len(ollama_messages))):
                if ollama_messages[i]["role"] == "user":
                    ollama_messages[i]["images"] = images
                    print(f"🖼️ Added {len(images)} images to user message")
                    break
        
        response = ollama.chat(
            model=self.model_name,
            messages=ollama_messages,
            format="json"
        )
        
        return response['message']['content']
    
    def _extract_images_from_content(self, content: str) -> List[bytes]:
        """Extract base64 images from tool result content"""
        images = [] 
        try:
            if "Tool result:" in content:
                json_start = content.find("{")
                if json_start != -1:
                    json_str = content[json_start:]
                    try:
                        data = json.loads(json_str)
                        
                        if "image" in data and isinstance(data["image"], dict):
                            if "data" in data["image"]:
                                image_data = base64.b64decode(data["image"]["data"])
                                images.append(image_data)
                                print(f"🖼️ Extracted image: {data['image'].get('filename', 'unknown')}")
                    except json.JSONDecodeError:
                        pass
        except Exception as e:
            print(f"⚠️ Error extracting images: {e}")
        
        return images 