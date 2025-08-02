"""
Emergency tools provider - consolidates all emergency-related functionality.
Implements the ToolProvider protocol for easy registration.
"""
import random
import base64
import datetime
from pathlib import Path
from typing import Dict, Any, List
from ..base.tool_registry import ToolProvider, ToolDefinition

class EmergencyToolsProvider(ToolProvider):
    """Provider for all emergency-related tools"""
    
    def get_tools(self) -> List[ToolDefinition]:
        """Return all emergency tools"""
        return [
            # Crisis response tools
            ToolDefinition(
                name="call_emergency_contact",
                description="Call a predefined emergency contact",
                parameters={
                    "contact_type": {"type": "string", "enum": ["primary", "secondary", "medical"]}
                },
                func=self.call_emergency_contact,
                domain="emergency"
            ),
            ToolDefinition(
                name="activate_alarm",
                description="Trigger a loud alarm to alert nearby people",
                parameters={
                    "duration_seconds": {"type": "integer", "default": 60}
                },
                func=self.activate_alarm,
                domain="emergency"
            ),
            ToolDefinition(
                name="log_incident",
                description="Log the crisis incident with timestamp",
                parameters={
                    "incident_type": {"type": "string"},
                    "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]}
                },
                func=self.log_incident,
                domain="emergency"
            ),
            
            # One-minute tools (health monitoring)
            ToolDefinition(
                name="get_health_metrics",
                description="Returns the current health metrics of the user (heart_rate, blood_pressure, blood_oxygen)",
                parameters={},
                func=self.get_health_metrics,
                domain="emergency",
                async_func=True
            ),
            ToolDefinition(
                name="get_user_location",
                description="Returns the current location of the user (latitude, longitude)",
                parameters={},
                func=self.get_user_location,
                domain="emergency",
                async_func=True
            ),
            ToolDefinition(
                name="get_audio_input",
                description="Returns simulated audio input from the user indicating emergency situations",
                parameters={},
                func=self.get_audio_input,
                domain="emergency",
                async_func=True
            ),
            ToolDefinition(
                name="get_video_input",
                description="Returns a sample emergency image for multimodal analysis",
                parameters={},
                func=self.get_video_input,
                domain="emergency",
                async_func=True
            ),
            ToolDefinition(
                name="get_user_details",
                description="Returns detailed personal and medical information about the user",
                parameters={},
                func=self.get_user_details,
                domain="emergency",
                async_func=True
            )
        ]
    
    # Crisis response tools (from original emergency_tools.py)
    
    def call_emergency_contact(self, contact_type: str = "primary") -> Dict[str, Any]:
        """Call a predefined emergency contact"""
        print(f"🚨 CALLING: {contact_type} emergency contact...")
        return {
            "status": "success", 
            "message": f"Called {contact_type} contact",
            "contact_type": contact_type,
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    def activate_alarm(self, duration_seconds: int = 60) -> Dict[str, Any]:
        """Trigger a loud alarm to alert nearby people"""
        print(f"🔔 ALARM: Activating for {duration_seconds} seconds...")
        return {
            "status": "success", 
            "message": f"Alarm activated for {duration_seconds}s",
            "duration": duration_seconds,
            "timestamp": datetime.datetime.now().isoformat()
        }
    
    def log_incident(self, incident_type: str = "unknown", severity: str = "medium") -> Dict[str, Any]:
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
    
    # One-minute tools (health monitoring)
    
    async def get_health_metrics(self) -> Dict[str, Any]:
        """Returns the current health metrics of the user"""
        print("✅ Getting health metrics")
        return {
            "heart_rate": 100,
            "blood_pressure": 120,
            "blood_oxygen": 95,
        }
    
    async def get_user_location(self) -> Dict[str, Any]:
        """Returns the current location of the user"""
        print("📍 Getting user location")
        return {
            "latitude": 40.7128,
            "longitude": -74.0060,
        }
    
    async def get_audio_input(self) -> Dict[str, Any]:
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
    
    async def get_video_input(self) -> Dict[str, Any]:
        """Returns a sample emergency image for multimodal analysis"""
        print("📹 Getting video input")
        
        # Get the path to the sample_images folder
        current_dir = Path(__file__).parent.parent
        sample_images_dir = current_dir / "stuff" / "sample_images"
        
        # Get all image files in the directory
        image_files = [
            "example_1.jpeg",
            "example_2.jpg", 
            "example_3.jpg",
            "example_5.jpg",
            "example_6.jpg"
        ]
        
        # Randomly select an image
        selected_image = random.choice(image_files)
        image_path = sample_images_dir / selected_image
        
        # Read and encode the image for multimodal processing
        try:
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                image_base64 = base64.b64encode(image_data).decode('utf-8')
                
            # Determine mime type based on file extension
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
            # Fallback to text description if image loading fails
            return {
                "error": f"Could not load image {selected_image}",
                "fallback_description": "Unable to access video feed - visual analysis not available"
            }
    
    async def get_user_details(self) -> Dict[str, Any]:
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