import random
import os
import base64
from pathlib import Path
from typing import Dict, Any

async def get_health_metrics() -> Dict[str, Any]:
    """Returns the current health metrics of the user.

    Returns:
        dict: Contains heart_rate, blood_pressure, and blood_oxygen values.
    """
    print("✅ Getting health metrics")
    return {
        "heart_rate": 100,
        "blood_pressure": 120,
        "blood_oxygen": 95,
    }

async def get_user_location() -> Dict[str, Any]:
    """Returns the current location of the user.

    Returns:
        dict: Contains latitude and longitude coordinates.
    """
    print("📍 Getting user location")
    return {
        "latitude": 40.7128,
        "longitude": -74.0060,
    }

async def get_audio_input() -> Dict[str, Any]:
    """Returns simulated audio input from the user indicating emergency situations.

    Returns:
        dict: Contains audio field with a randomly selected emergency phrase.
    """
    print("🎙️ Getting audio input")
    situations = [
        "Ah! I think I'm having a heart attack",
        "Cough, cough, cough",
        "Ahh!!! My chest is killing me",
        "I feel some pressure in my chest",
        "Please help me, I'm dying",
    ]
    return {"audio": random.choice(situations)}

async def get_video_input() -> Dict[str, Any]:
    """Returns a sample emergency image for multimodal analysis.

    Returns:
        dict: Contains image data in base64 format and metadata for direct model processing.
    """
    print("📹 Getting video input")
    
    current_dir = Path(__file__).parent.parent
    sample_images_dir = current_dir / "stuff" / "sample_images"
    
    image_files = [
        "example_1.jpeg",
        "example_2.jpg", 
        "example_3.jpg",
        "example_5.jpg",
        "example_6.jpg"
    ]
    
    selected_image = random.choice(image_files)
    image_path = sample_images_dir / selected_image
    
    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
        mime_type = "image/jpeg" if selected_image.endswith(('.jpg', '.jpeg')) else "image/png"
        
        return {
            "image": {
                "data": image_base64,
                "mime_type": mime_type,
                "filename": selected_image
            },
            "description": f"Emergency scene captured from video feed: {selected_image}"
        }
        
    except Exception as e:
        print(f"Error loading image {selected_image}: {e}")
        return {
            "error": f"Could not load image {selected_image}",
            "fallback_description": "Unable to access video feed - visual analysis not available"
        }

async def get_user_details() -> Dict[str, Any]:
    """Returns detailed personal and medical information about the user.

    Returns:
        dict: Contains personal details including name, age, gender, blood_type, 
              medical_history, current_medications, allergies, and medical_conditions.
    """
    print("👤 Getting user details")
    return {
        "name": "John Doe",
        "age": 30,
        "gender": "male",
        "blood_type": "A+",
        "medical_history": "None",
        "current_medications": "None",
        "allergies": "None",
        "medical_conditions": "None",
    }