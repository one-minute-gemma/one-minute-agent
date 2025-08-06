"""
Message Types and Structures for Inter-Agent Communication

Defines all message formats, priorities, and metadata structures
used in emergency response agent coordination.
"""

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid

class AgentRole(Enum):
    """Roles in the emergency response system"""
    VICTIM_ASSISTANT = "victim_assistant"
    OPERATOR = "operator"
    SYSTEM = "system"

class MessageType(Enum):
    """Types of inter-agent messages"""
    SITUATION_UPDATE = "situation_update"      # Victim info to Operator
    DISPATCH_UPDATE = "dispatch_update"        # Operator info to Victim
    STATUS_UPDATE = "status_update"            # General status changes
    EMERGENCY_ESCALATION = "emergency_escalation"  # Critical escalations
    COORDINATION_REQUEST = "coordination_request"   # Request for coordination
    ACKNOWLEDGMENT = "acknowledgment"          # Message received confirmation

class Priority(Enum):
    """Message priority levels"""
    CRITICAL = 1    # Life-threatening, immediate response required
    HIGH = 2        # Urgent, response needed within 1 minute
    MEDIUM = 3      # Important, response needed within 5 minutes
    LOW = 4         # Informational, no immediate response required

@dataclass
class InterAgentMessage:
    """Base structure for all inter-agent messages"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    sender: AgentRole = AgentRole.SYSTEM
    recipient: AgentRole = AgentRole.SYSTEM
    message_type: MessageType = MessageType.STATUS_UPDATE
    priority: Priority = Priority.MEDIUM
    content: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    requires_response: bool = False
    response_timeout_seconds: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for serialization"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'sender': self.sender.value,
            'recipient': self.recipient.value,
            'message_type': self.message_type.value,
            'priority': self.priority.value,
            'content': self.content,
            'metadata': self.metadata,
            'requires_response': self.requires_response,
            'response_timeout_seconds': self.response_timeout_seconds
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InterAgentMessage':
        """Create message from dictionary"""
        return cls(
            id=data['id'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            sender=AgentRole(data['sender']),
            recipient=AgentRole(data['recipient']),
            message_type=MessageType(data['message_type']),
            priority=Priority(data['priority']),
            content=data['content'],
            metadata=data['metadata'],
            requires_response=data['requires_response'],
            response_timeout_seconds=data.get('response_timeout_seconds')
        )

@dataclass
class SituationUpdate(InterAgentMessage):
    """Victim Assistant -> Operator: Critical situation updates"""
    def __init__(self, 
                 situation_description: str,
                 victim_status: Dict[str, Any],
                 environmental_hazards: List[str] = None,
                 immediate_needs: List[str] = None,
                 priority: Priority = Priority.HIGH,
                 **kwargs):
        super().__init__(
            sender=AgentRole.VICTIM_ASSISTANT,
            recipient=AgentRole.OPERATOR,
            message_type=MessageType.SITUATION_UPDATE,
            priority=priority,
            content={
                'situation_description': situation_description,
                'victim_status': victim_status,
                'environmental_hazards': environmental_hazards or [],
                'immediate_needs': immediate_needs or [],
            },
            requires_response=True,
            response_timeout_seconds=60,  # Operator should respond within 1 minute
            **kwargs
        )

@dataclass
class DispatchUpdate(InterAgentMessage):
    """Operator -> Victim Assistant: First responder and dispatch information"""
    def __init__(self,
                 responder_eta: Optional[int],
                 responder_types: List[str],
                 instructions_for_victim: str,
                 dispatch_status: str,
                 priority: Priority = Priority.HIGH,
                 **kwargs):
        super().__init__(
            sender=AgentRole.OPERATOR,
            recipient=AgentRole.VICTIM_ASSISTANT,
            message_type=MessageType.DISPATCH_UPDATE,
            priority=priority,
            content={
                'responder_eta': responder_eta,  # Minutes until arrival
                'responder_types': responder_types,  # ['fire', 'medical', 'police']
                'instructions_for_victim': instructions_for_victim,
                'dispatch_status': dispatch_status,  # 'dispatched', 'en_route', 'on_scene'
            },
            requires_response=False,
            **kwargs
        )

@dataclass
class StatusUpdate(InterAgentMessage):
    """General status updates between agents"""
    def __init__(self,
                 status: str,
                 details: Dict[str, Any] = None,
                 priority: Priority = Priority.MEDIUM,
                 sender: AgentRole = AgentRole.SYSTEM,
                 recipient: AgentRole = AgentRole.SYSTEM,
                 **kwargs):
        super().__init__(
            sender=sender,
            recipient=recipient,
            message_type=MessageType.STATUS_UPDATE,
            priority=priority,
            content={
                'status': status,
                'details': details or {}
            },
            **kwargs
        )

@dataclass
class EmergencyEscalation(InterAgentMessage):
    """Critical escalations requiring immediate attention"""
    def __init__(self,
                 escalation_reason: str,
                 critical_details: Dict[str, Any],
                 recommended_actions: List[str],
                 sender: AgentRole,
                 **kwargs):
        super().__init__(
            sender=sender,
            recipient=AgentRole.OPERATOR if sender == AgentRole.VICTIM_ASSISTANT else AgentRole.VICTIM_ASSISTANT,
            message_type=MessageType.EMERGENCY_ESCALATION,
            priority=Priority.CRITICAL,
            content={
                'escalation_reason': escalation_reason,
                'critical_details': critical_details,
                'recommended_actions': recommended_actions
            },
            requires_response=True,
            response_timeout_seconds=30,  # Critical - 30 second response time
            **kwargs
        )

# Message creation helper functions
def create_situation_update(
    situation: str,
    victim_status: Dict[str, Any],
    hazards: List[str] = None,
    needs: List[str] = None,
    priority: Priority = Priority.HIGH
) -> SituationUpdate:
    """Helper to create situation update messages"""
    return SituationUpdate(
        situation_description=situation,
        victim_status=victim_status,
        environmental_hazards=hazards,
        immediate_needs=needs,
        priority=priority
    )

def create_dispatch_update(
    eta: Optional[int],
    responder_types: List[str],
    instructions: str,
    status: str = "dispatched",
    priority: Priority = Priority.HIGH
) -> DispatchUpdate:
    """Helper to create dispatch update messages"""
    return DispatchUpdate(
        responder_eta=eta,
        responder_types=responder_types,
        instructions_for_victim=instructions,
        dispatch_status=status,
        priority=priority
    )

def create_emergency_escalation(
    reason: str,
    details: Dict[str, Any],
    actions: List[str],
    sender: AgentRole
) -> EmergencyEscalation:
    """Helper to create emergency escalation messages"""
    return EmergencyEscalation(
        escalation_reason=reason,
        critical_details=details,
        recommended_actions=actions,
        sender=sender
    ) 