"""
Emergency tools provider - consolidates all emergency-related functionality.
Implements the ToolProvider protocol for easy registration.
"""
import random
import base64
import datetime
from pathlib import Path
from typing import Dict, Any, List
from nagents.base.tool_registry import ToolProvider, ToolDefinition

class EmergencyToolsProvider(ToolProvider):
    """Provider for all emergency-related tools"""
    ...
    
# Crisis response tools

def call_emergency_contact(contact_type: str = "primary") -> Dict[str, Any]:
    """Call a predefined emergency contact"""
    print(f"🚨 CALLING: {contact_type} emergency contact...")
    return {
        "status": "success", 
        "message": f"Called {contact_type} contact",
        "contact_type": contact_type,
        "timestamp": datetime.datetime.now().isoformat()
    }

def activate_alarm(duration_seconds: int = 60) -> Dict[str, Any]:
    """Trigger a loud alarm to alert nearby people"""
    print(f"🔔 ALARM: Activating for {duration_seconds} seconds...")
    return {
        "status": "success", 
        "message": f"Alarm activated for {duration_seconds}s",
        "duration": duration_seconds,
        "timestamp": datetime.datetime.now().isoformat()
    }

def log_incident(incident_type: str = "unknown", severity: str = "medium") -> Dict[str, Any]:
    """Log the crisis incident with timestamp"""
    timestamp = datetime.datetime.now().isoformat()
    incident_id = f"INC-{timestamp.replace(':', '').replace('-', '').replace('.', '')}"
    
    print(f"📝 LOGGED: {severity} {incident_type} incident - {incident_id}")
    return {
        "status": "success", 
        "incident_id": incident_id,
        "incident_type": incident_type,
        "severity": severity,
        "logged_at": timestamp
    }

# One-minute tools

async def get_health_metrics() -> Dict[str, Any]:
    """Returns the current health metrics of the user"""
    print("✅ Getting health metrics")
    return {
        "heart_rate": 100,
        "blood_pressure": 120,
        "blood_oxygen": 95,
    }

async def get_user_location() -> Dict[str, Any]:
    """Returns the current location of the user"""
    print("📍 Getting user location")
    return {
        "latitude": 40.7128,
        "longitude": -74.0060,
    }

async def get_audio_input() -> Dict[str, Any]:
    """Returns simulated audio input from the user indicating emergency situations"""
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
    """Returns a sample emergency image for multimodal analysis"""
    print("📹 Getting video input")
    
    current_dir = Path(__file__).parent.parent
    sample_images_dir = current_dir / "one-minute-agent" / "stuff" / "sample_images"
    
    image_files = [
        "example_1.jpeg",
        "example_2.jpg", 
        "example_3.jpg",
        "example_5.jpg",
        "example_6.jpg"
    ]
    
    try:
        selected_image = random.choice(image_files)
        image_path = sample_images_dir / selected_image
        
        print(f"📹 Loading image: {image_path}")
        print(f"📹 Image exists: {image_path.exists()}")

        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
        mime_type = "image/jpeg" if selected_image.endswith(('.jpg', '.jpeg')) else "image/png"
        
        result = {
            "image": {
                "data": image_base64,
                "mime_type": mime_type,
                "filename": selected_image
            },
            "description": f"Emergency scene captured from video feed: {selected_image}"
        }
        
        print(f"📹 Returning image data - filename: {selected_image}, size: {len(image_base64)} chars")
        return result
        
    except Exception as e:
        print(f"Error loading image {selected_image}: {e}")

        return {
            "error": f"Could not load image {selected_image}",
            "fallback_description": "Unable to access video feed - visual analysis not available"
        }

async def get_user_details() -> Dict[str, Any]:
    """Returns detailed personal and medical information about the user"""
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

tools = [
    get_health_metrics,
    get_user_location,
    get_audio_input,
    get_video_input,
    get_user_details,
    call_emergency_contact,
    activate_alarm,
    log_incident
]

emergency_tools = EmergencyToolsProvider().get_tools(tools, "emergency")