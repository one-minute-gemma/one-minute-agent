"""
Communication Tools for Agents

Provides tool functions that agents can use to send messages to each other.
"""

from typing import List, Dict, Any, Union
from nagents.base.tool_registry import ToolProvider

from .message_bus import get_message_bus
from .event_logger import get_event_logger
from .message_types import (
    AgentRole, MessageType, Priority,
    create_situation_update, create_dispatch_update, 
    StatusUpdate, EmergencyEscalation
)


class CommunicationToolsProvider(ToolProvider):
    """Provider for communication tools"""
    ...


# Victim Assistant Communication Tools

def send_situation_update(
    situation_description: str,
    victim_status: Union[Dict[str, Any], str] = None,
    environmental_hazards: Union[List[str], str] = None,
    immediate_needs: Union[List[str], str] = None,
    priority: str = "HIGH",
    **kwargs  # This will catch any typos like 'environmental_hazaards'
) -> Dict[str, Any]:
    """
    Send a situation update to the 911 operator.
    
    Args:
        situation_description: Clear description of the emergency situation
        victim_status: Dictionary with victim information or string description
        environmental_hazards: List of environmental dangers or string description
        immediate_needs: List of immediate assistance needed or string description
        priority: Message priority (CRITICAL, HIGH, MEDIUM, LOW)
        **kwargs: Catches any parameter typos and ignores them gracefully
        
    Returns:
        Confirmation of message sent
    """
    try:
        # Handle flexible input types
        if isinstance(victim_status, str):
            victim_status = {"description": victim_status}
        elif victim_status is None:
            victim_status = {"status": "unknown"}
            
        if isinstance(environmental_hazards, str):
            environmental_hazards = [environmental_hazards]
        elif environmental_hazards is None:
            environmental_hazards = []
            
        # FIXED: Handle common typos
        if 'environmental_hazaards' in kwargs:
            environmental_hazards = kwargs['environmental_hazaards']
            if isinstance(environmental_hazards, str):
                environmental_hazards = [environmental_hazards]
        
        if isinstance(immediate_needs, str):
            immediate_needs = [immediate_needs]
        elif immediate_needs is None:
            immediate_needs = []
        # Parse priority
        try:
            priority_enum = Priority[priority.upper()]
        except (KeyError, AttributeError):
            priority_enum = Priority.HIGH
            
        message = create_situation_update(
            situation=situation_description,
            victim_status=victim_status,
            hazards=environmental_hazards,
            needs=immediate_needs,
            priority=priority_enum
        )
        
        message_bus = get_message_bus()
        success = message_bus.publish(message)
        
        return {
            "success": success,
            "message_id": message.id,
            "sent_to": "911 Operator",
            "priority": priority_enum.name,
            "message": f"Situation update sent: {situation_description[:50]}..."
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to send situation update: {str(e)}",
            "message": "Communication tool error - please try again"
        }

def request_emergency_escalation(
    escalation_reason: str,
    critical_details: Union[Dict[str, Any], str] = None,
    **kwargs  # Catch any misspelled parameters
) -> Dict[str, Any]:
    """
    Send critical emergency escalation to operator.
    
    Args:
        escalation_reason: Reason for escalation
        critical_details: Critical situation details
        **kwargs: Flexible parameters including recommended_actions (and common misspellings)
        
    Returns:
        Confirmation of escalation sent
    """
    try:
        # Handle flexible input types
        if isinstance(critical_details, str):
            critical_details = {"description": critical_details}
        elif critical_details is None:
            critical_details = {"reason": escalation_reason}
        
        # Extract recommended actions from kwargs, handling all possible misspellings
        recommended_actions = None
        possible_keys = [
            'recommended_actions',
            'recommendeed_actions',
            'recommendeeed_actions',  # Handle triple 'e'
            'reccomended_actions',
            'recomended_actions',
            'actions',
            'suggested_actions'
        ]
        
        for key in possible_keys:
            if key in kwargs and kwargs[key] is not None:
                recommended_actions = kwargs[key]
                break
        
        # Default if no actions provided
        if recommended_actions is None:
            recommended_actions = ["immediate emergency response required"]
        elif isinstance(recommended_actions, str):
            recommended_actions = [recommended_actions]
        
        message = EmergencyEscalation(
            escalation_reason=escalation_reason,
            critical_details=critical_details,
            recommended_actions=recommended_actions,
            sender=AgentRole.VICTIM_ASSISTANT
        )
        
        message_bus = get_message_bus()
        success = message_bus.publish(message)
        
        return {
            "success": success,
            "message_id": message.id,
            "escalation_sent": True,
            "priority": "CRITICAL",
            "message": f"Emergency escalation sent: {escalation_reason[:50]}..."
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to send escalation: {str(e)}",
            "message": "Emergency escalation failed - please try again"
        }

def send_victim_status_update(
    status: str,
    details: Union[Dict[str, Any], str] = None
) -> Dict[str, Any]:
    """
    Send a general status update from victim assistant.
    
    Args:
        status: Status message
        details: Additional status details
        
    Returns:
        Confirmation of status sent
    """
    try:
        # Handle flexible input types
        if isinstance(details, str):
            details = {"description": details}
        elif details is None:
            details = {}
        
        message = StatusUpdate(
            status=status,
            details=details,
            sender=AgentRole.VICTIM_ASSISTANT,
            recipient=AgentRole.OPERATOR
        )
        
        message_bus = get_message_bus()
        success = message_bus.publish(message)
        
        return {
            "success": success,
            "message_id": message.id,
            "status_sent": True,
            "message": f"Status update sent: {status[:50]}..."
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to send status: {str(e)}",
            "message": "Status update failed - please try again"
        }

# Operator Communication Tools
def send_dispatch_update(
    responder_eta: Union[int, str] = None,
    responder_types: Union[List[str], str] = None,
    instructions_for_victim: str = "",
    dispatch_status: str = "dispatched"
) -> Dict[str, Any]:
    """
    Send dispatch update to victim assistant.
    
    Args:
        responder_eta: Estimated time of arrival in minutes
        responder_types: Types of responders (fire, medical, police)
        instructions_for_victim: Instructions for the victim
        dispatch_status: Status of dispatch (dispatched, en_route, on_scene)
        
    Returns:
        Confirmation of dispatch update sent
    """
    try:
        # Handle flexible input types
        if isinstance(responder_eta, str):
            try:
                responder_eta = int(responder_eta)
            except ValueError:
                responder_eta = None
                
        if isinstance(responder_types, str):
            responder_types = [responder_types]
        elif responder_types is None:
            responder_types = []
        
        message = create_dispatch_update(
            eta=responder_eta,
            responder_types=responder_types,
            instructions=instructions_for_victim,
            status=dispatch_status
        )
        
        message_bus = get_message_bus()
        success = message_bus.publish(message)
        
        return {
            "success": success,
            "message_id": message.id,
            "dispatch_update_sent": True,
            "eta": responder_eta,
            "status": dispatch_status,
            "message": f"Dispatch update sent: {dispatch_status}, ETA {responder_eta}min"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to send dispatch update: {str(e)}",
            "message": "Dispatch update failed - please try again"
        }

def send_operator_status(
    status: str,
    details: Union[Dict[str, Any], str] = None
) -> Dict[str, Any]:
    """
    Send operator status update.
    
    Args:
        status: Status message
        details: Additional details
        
    Returns:
        Confirmation of status sent
    """
    try:
        # Handle flexible input types
        if isinstance(details, str):
            details = {"description": details}
        elif details is None:
            details = {}
        
        message = StatusUpdate(
            status=status,
            details=details,
            sender=AgentRole.OPERATOR,
            recipient=AgentRole.VICTIM_ASSISTANT
        )
        
        message_bus = get_message_bus()
        success = message_bus.publish(message)
        
        return {
            "success": True,
            "message_id": message.id,
            "operator_status_sent": True,
            "message": f"Operator status sent: {status[:50]}..."
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to send status: {str(e)}",
            "message": "Operator status update failed - please try again"
        }


# Tool collections for each agent type
victim_communication_tools = [
    send_situation_update,
    request_emergency_escalation,
    send_victim_status_update
]

operator_communication_tools = [
    send_dispatch_update,
    send_operator_status
]


def create_victim_communication_tools():
    """Create communication tools for victim assistant agent"""
    provider = CommunicationToolsProvider()
    return provider.get_tools(victim_communication_tools, "communication")


def create_operator_communication_tools():
    """Create communication tools for operator agent"""
    provider = CommunicationToolsProvider()
    return provider.get_tools(operator_communication_tools, "communication")