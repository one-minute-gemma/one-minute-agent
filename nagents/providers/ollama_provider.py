"""
Ollama model provider implementation.
Handles communication with Ollama models.
"""
import ollama
import json
import base64
from typing import List
from ..base.agent import ModelProvider, Message
import os
import requests
import logging
import time

class OllamaProvider(ModelProvider):
    """Ollama implementation of ModelProvider protocol"""
    
    def __init__(self, model_name: str = None, host: str = None, request_timeout_seconds: int = None):
        self.model_name = model_name
        env_host = os.environ.get('OLLAMA_HOST', 'http://127.0.0.1:11434')
        raw_host = host or env_host
        if not raw_host.startswith('http'):
            raw_host = f"http://{raw_host}"
        # Never try to connect to 0.0.0.0 — that's a bind address
        raw_host = raw_host.replace('0.0.0.0', '127.0.0.1')
        self.host = raw_host
        # Allow override via env, default to 300s for slow first-Gen warmup
        env_timeout = os.environ.get('OLLAMA_CLIENT_TIMEOUT_SECONDS')
        self.request_timeout_seconds = int(env_timeout) if env_timeout else (request_timeout_seconds or 300)
        
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug(f"Initialized with model={self.model_name}, host={self.host}, timeout={self.request_timeout_seconds}s")
    
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
                self.logger.debug(f"Found {len(msg_images)} image(s) in message from {msg.role}")
            
            ollama_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        if images and ollama_messages:
            for i in reversed(range(len(ollama_messages))):
                if ollama_messages[i]["role"] == "user":
                    ollama_messages[i]["images"] = images
                    self.logger.debug(f"Attached {len(images)} image(s) to the last user message")
                    break
        
        # Prefer HTTP API with explicit timeout to avoid hanging on HF Spaces
        url = f"{self.host.rstrip('/')}/api/chat"
        payload = {
            "model": self.model_name,
            "messages": ollama_messages,
            "stream": False,
            "format": "json",
            # Small first output to reduce cold-start latency; model can continue in subsequent turns
            "options": {"num_predict": 128, "temperature": 0},
            # Keep the model in memory for a while after first load
            "keep_alive": "10m",
        }
        start_time = time.time()
        try:
            self.logger.info(f"POST {url} model={self.model_name} timeout={self.request_timeout_seconds}s")
            response = requests.post(url, json=payload, timeout=(5, self.request_timeout_seconds))
            elapsed = (time.time() - start_time) * 1000
            self.logger.info(f"POST {url} -> {response.status_code} in {elapsed:.0f} ms")
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict):
                message = data.get('message', {})
                content = message.get('content') if isinstance(message, dict) else None
                # Log only the first 200 chars to avoid spam
                if content:
                    self.logger.debug(f"Response content (truncated): {content[:200]}")
                return content or json.dumps(data)
            return json.dumps(data)
        except requests.Timeout:
            elapsed = (time.time() - start_time) * 1000
            self.logger.error(f"Ollama request timed out after {elapsed:.0f} ms (timeout={self.request_timeout_seconds}s)")
            raise RuntimeError("Ollama request timed out. The model may still be loading into memory. Please try again shortly.")
        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            self.logger.exception(f"Ollama request failed after {elapsed:.0f} ms: {e}")
            raise RuntimeError(f"Ollama request failed: {e}")
    
    def _extract_images_from_content(self, content: str) -> List[bytes]:
        """Extract base64 images from tool result content (return base64 strings)"""
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
                                # Keep as base64 string for HTTP API
                                image_b64 = data["image"].get("data")
                                if image_b64:
                                    images.append(image_b64)
                                    self.logger.debug(f"Extracted image: {data['image'].get('filename', 'unknown')}")
                    except json.JSONDecodeError:
                        pass
        except Exception as e:
            self.logger.warning(f"Error extracting images: {e}")
        
        return images 