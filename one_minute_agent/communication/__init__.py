"""
Inter-Agent Communication System

Provides structured message passing, event logging, and coordination
between Victim Assistant and Operator agents in emergency scenarios.
"""

from .message_bus import MessageBus, EmergencyMessageBus, get_message_bus
from .message_types import (
    MessageType, Priority, AgentRole,
    InterAgentMessage, SituationUpdate, DispatchUpdate, 
    StatusUpdate, EmergencyEscalation,
    create_situation_update, create_dispatch_update, create_emergency_escalation
)
from .communication_tools import (
    create_victim_communication_tools,
    create_operator_communication_tools
)
from .event_logger import EventLogger, LogEntry, LogLevel, get_event_logger
from .coordination_system import CoordinationSystem, get_coordination_system

__all__ = [
    # Core message bus
    'MessageBus', 'EmergencyMessageBus', 'get_message_bus',
    
    # Message types and structures
    'MessageType', 'Priority', 'AgentRole',
    'InterAgentMessage', 'SituationUpdate', 'DispatchUpdate',
    'StatusUpdate', 'EmergencyEscalation',
    'create_situation_update', 'create_dispatch_update', 'create_emergency_escalation',
    
    # Communication tools for agents
    'create_victim_communication_tools',
    'create_operator_communication_tools',
    
    # Event logging
    'EventLogger', 'LogEntry', 'LogLevel', 'get_event_logger',
    
    # Coordination system
    'CoordinationSystem', 'get_coordination_system'
] 