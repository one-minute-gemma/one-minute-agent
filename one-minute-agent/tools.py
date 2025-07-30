import random
from typing import Dict, List, Callable, Any

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
    """Returns simulated video input describing emergency visual situations.

    Returns:
        dict: Contains video field with a randomly selected emergency scene description.
    """
    print("📹 Getting video input")
    situations = [
        "The person is lying on the ground, not moving",
        "The person is unconscious, not moving",
        "The person is unresponsive, not moving",
        "The person is not breathing, not moving",
    ]
    return {"video": random.choice(situations)}

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

tools: List[Callable] = [
    get_health_metrics,
    get_user_location,
    get_audio_input,
    get_video_input,
    get_user_details,
]