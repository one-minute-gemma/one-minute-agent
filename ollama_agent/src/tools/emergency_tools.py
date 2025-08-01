"""
Basic emergency response tools for Feature 0.
These are dummy implementations to establish the function-calling pattern.
"""
import datetime
from typing import Dict, Any

def get_available_tools() -> Dict[str, Dict]:
    """Return tool definitions for the model"""
    return {
        "call_emergency_contact": {
            "name": "call_emergency_contact",
            "description": "Call a predefined emergency contact",
            "parameters": {
                "contact_type": {"type": "string", "enum": ["primary", "secondary", "medical"]}
            }
        },
        "activate_alarm": {
            "name": "activate_alarm", 
            "description": "Trigger a loud alarm to alert nearby people",
            "parameters": {
                "duration_seconds": {"type": "integer", "default": 60}
            }
        },
        "log_incident": {
            "name": "log_incident",
            "description": "Log the crisis incident with timestamp",
            "parameters": {
                "incident_type": {"type": "string"},
                "severity": {"type": "string", "enum": ["low", "medium", "high", "critical"]}
            }
        }
    }

def execute_tool(tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a crisis response tool. Currently dummy implementations."""
    
    if tool_name == "call_emergency_contact":
        contact_type = args.get("contact_type", "primary")
        print(f"🚨 DUMMY: Calling {contact_type} emergency contact...")
        return {"status": "success", "message": f"Called {contact_type} contact", "dummy": True}
    
    elif tool_name == "activate_alarm":
        duration = args.get("duration_seconds", 60)
        print(f"🔔 DUMMY: Activating alarm for {duration} seconds...")
        return {"status": "success", "message": f"Alarm activated for {duration}s", "dummy": True}
    
    elif tool_name == "log_incident":
        incident_type = args.get("incident_type", "unknown")
        severity = args.get("severity", "medium")
        timestamp = datetime.datetime.now().isoformat()
        print(f"📝 DUMMY: Logging {severity} {incident_type} incident at {timestamp}")
        return {
            "status": "success", 
            "incident_id": f"INC-{timestamp}", 
            "logged_at": timestamp,
            "dummy": True
        }
    
    else:
        return {"status": "error", "message": f"Unknown tool: {tool_name}"}