"""
Coordination System for Inter-Agent Communication

Central coordination system that manages agent registration and message routing.
"""

from typing import Dict, Optional, Any
from datetime import datetime

from .message_bus import get_message_bus, EmergencyMessageBus
from .event_logger import get_event_logger, LogLevel
from .message_types import AgentRole, InterAgentMessage


class CoordinationSystem:
    """Central coordination system for emergency response agents"""
    
    def __init__(self):
        self._agents: Dict[AgentRole, Any] = {}
        self._message_bus = get_message_bus()
        self._event_logger = get_event_logger()
        
        # Set up message bus event logging
        self._message_bus.add_event_listener(self._log_message_event)
    
    def register_agent(self, role: AgentRole, agent: Any):
        """Register an agent with the coordination system"""
        self._agents[role] = agent
        self._event_logger.log_event(
            LogLevel.INFO,
            "COORDINATION",
            f"Agent registered: {role.value}",
            {"role": role.value, "timestamp": datetime.now().isoformat()}
        )
        
        # Subscribe agent to receive messages
        self._message_bus.subscribe(role, self._handle_agent_message)
    
    def get_agent(self, role: AgentRole) -> Optional[Any]:
        """Get registered agent by role"""
        return self._agents.get(role)
    
    def get_registered_agents(self) -> Dict[AgentRole, Any]:
        """Get all registered agents"""
        return self._agents.copy()
    
    def send_message(self, message: InterAgentMessage) -> bool:
        """Send a message through the coordination system"""
        return self._message_bus.publish(message)
    
    def get_message_history(self, limit: Optional[int] = None):
        """Get message history from the bus"""
        return self._message_bus.get_message_history(limit)
    
    def get_log_entries(self, limit: Optional[int] = None):
        """Get event log entries"""
        return self._event_logger.get_entries(limit)
    
    def _handle_agent_message(self, message: InterAgentMessage):
        """Handle incoming message for an agent"""
        recipient_agent = self._agents.get(message.recipient)
        if recipient_agent:
            # Log that message was delivered
            self._event_logger.log_event(
                LogLevel.INFO,
                "COORDINATION",
                f"Message delivered to {message.recipient.value}",
                {"message_id": message.id, "message_type": message.message_type.value}
            )
        else:
            # Log that recipient was not found
            self._event_logger.log_event(
                LogLevel.WARNING,
                "COORDINATION",
                f"Recipient not found: {message.recipient.value}",
                {"message_id": message.id}
            )
    
    def _log_message_event(self, message: InterAgentMessage):
        """Log message events from the bus"""
        self._event_logger.log_message(message)


# Global coordination system instance
_coordination_system: Optional[CoordinationSystem] = None

def get_coordination_system() -> CoordinationSystem:
    """Get the global coordination system instance"""
    global _coordination_system
    if _coordination_system is None:
        _coordination_system = CoordinationSystem()
    return _coordination_system
