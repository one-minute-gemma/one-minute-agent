"""
Message Bus Implementation for Inter-Agent Communication

Provides message passing infrastructure between emergency response agents.
"""

from typing import Dict, List, Callable, Optional
from datetime import datetime
import asyncio
import threading
from collections import defaultdict

from .message_types import InterAgentMessage, AgentRole, MessageType, Priority


class MessageBus:
    """Core message bus for inter-agent communication"""
    
    def __init__(self):
        self._subscribers: Dict[AgentRole, List[Callable]] = defaultdict(list)
        self._message_history: List[InterAgentMessage] = []
        self._lock = threading.Lock()
    
    def subscribe(self, role: AgentRole, callback: Callable[[InterAgentMessage], None]):
        """Subscribe to messages for a specific agent role"""
        with self._lock:
            self._subscribers[role].append(callback)
    
    def publish(self, message: InterAgentMessage) -> bool:
        """Publish a message to subscribers"""
        with self._lock:
            self._message_history.append(message)
            
            # Notify subscribers for the recipient role
            if message.recipient in self._subscribers:
                for callback in self._subscribers[message.recipient]:
                    try:
                        callback(message)
                    except Exception as e:
                        print(f"Error delivering message to subscriber: {e}")
                        
            return True
    
    def get_message_history(self, limit: Optional[int] = None) -> List[InterAgentMessage]:
        """Get message history, optionally limited to recent messages"""
        with self._lock:
            if limit:
                return self._message_history[-limit:]
            return self._message_history.copy()
    
    def clear_history(self):
        """Clear message history"""
        with self._lock:
            self._message_history.clear()


class EmergencyMessageBus(MessageBus):
    """Enhanced message bus for emergency scenarios with priority handling"""
    
    def __init__(self):
        super().__init__()
        self._priority_queue: Dict[Priority, List[InterAgentMessage]] = defaultdict(list)
        self._event_callbacks: List[Callable[[InterAgentMessage], None]] = []
    
    def add_event_listener(self, callback: Callable[[InterAgentMessage], None]):
        """Add a callback for all message events (for logging/monitoring)"""
        self._event_callbacks.append(callback)
    
    def publish(self, message: InterAgentMessage) -> bool:
        """Publish with priority handling and event logging"""
        with self._lock:
            # Add to priority queue
            self._priority_queue[message.priority].append(message)
            
            # Add to history
            self._message_history.append(message)
            
            # Notify event listeners
            for callback in self._event_callbacks:
                try:
                    callback(message)
                except Exception as e:
                    print(f"Error in event callback: {e}")
            
            # Deliver to subscribers
            if message.recipient in self._subscribers:
                for callback in self._subscribers[message.recipient]:
                    try:
                        callback(message)
                    except Exception as e:
                        print(f"Error delivering message to subscriber: {e}")
                        
            return True
    
    def get_priority_messages(self, priority: Priority) -> List[InterAgentMessage]:
        """Get messages by priority level"""
        with self._lock:
            return self._priority_queue[priority].copy()
    
    def get_critical_messages(self) -> List[InterAgentMessage]:
        """Get all critical priority messages"""
        return self.get_priority_messages(Priority.CRITICAL)


# Global message bus instance
_message_bus: Optional[EmergencyMessageBus] = None

def get_message_bus() -> EmergencyMessageBus:
    """Get the global message bus instance"""
    global _message_bus
    if _message_bus is None:
        _message_bus = EmergencyMessageBus()
    return _message_bus 