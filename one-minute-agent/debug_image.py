#!/usr/bin/env python3
"""
Debug script to test image handling with Ollama
"""
import sys
from pathlib import Path
import base64

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from nagents.providers.ollama_provider import OllamaProvider
from nagents.base.agent import Message

def test_image_direct():
    """Test sending image directly to Ollama"""
    print("🧪 Testing direct image sending to Ollama...")
    
    image_path = Path("stuff/sample_images/example_1.jpeg")
    if not image_path.exists():
        print(f"❌ Image not found: {image_path}")
        return
    
    with open(image_path, "rb") as f:
        image_data = f.read()
    
    print(f"✅ Loaded image: {image_path} ({len(image_data)} bytes)")
    
    # Test with provider
    provider = OllamaProvider("llava:latest")

    tool_result_content = f"""Tool result: {{
        "image": {{
            "data": "{base64.b64encode(image_data).decode('utf-8')}",
            "mime_type": "image/jpeg",
            "filename": "example_1.jpeg"
        }},
        "description": "Emergency scene captured from video feed"
    }}"""

    messages = [
        Message(role="user", content="Look at this emergency image and tell me EXACTLY what you see. Do not generate anything - just describe what is visible."),
        Message(role="system", content=tool_result_content)
    ]

    try:
        print("\n🧪 Testing with gemma3n:e2b...")
        response = provider.chat(messages, "You are analyzing an emergency image. Describe ONLY what you can see in the provided image. Do not generate or create anything.")
        print(f"🎯 gemma3n:e2b Response: {response}")
        
        # Test with llava for comparison
        print("\n🧪 Testing with llava for comparison...")
        provider_llava = OllamaProvider("llava")
        response_llava = provider_llava.chat(messages, "You are analyzing an emergency image. Describe ONLY what you can see in the provided image.")
        print(f"🎯 llava Response: {response_llava}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_image_direct() 