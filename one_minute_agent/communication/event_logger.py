"""
Event Logger for Inter-Agent Communication

Logs and tracks all communication events for monitoring and debugging.
"""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
import json

from .message_types import InterAgentMessage, AgentRole, MessageType, Priority


class LogLevel(Enum):
    """Log levels for event entries"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class LogEntry:
    """Individual log entry"""
    timestamp: datetime = field(default_factory=datetime.now)
    level: LogLevel = LogLevel.INFO
    source: str = "SYSTEM"
    message: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'level': self.level.value,
            'source': self.source,
            'message': self.message,
            'metadata': self.metadata
        }
    
    def format_for_display(self) -> str:
        """Format for display in UI"""
        time_str = self.timestamp.strftime("%H:%M:%S %p")
        return f"{time_str} {self.level.value} {self.message}"


class EventLogger:
    """Logger for inter-agent communication events"""
    
    def __init__(self, max_entries: int = 1000):
        self._entries: List[LogEntry] = []
        self._max_entries = max_entries
    
    def log_message(self, message: InterAgentMessage):
        """Log an inter-agent message"""
        entry = LogEntry(
            level=self._get_log_level_for_message(message),
            source=f"{message.sender.value.upper()}",
            message=self._format_message_for_log(message),
            metadata={
                'message_id': message.id,
                'message_type': message.message_type.value,
                'priority': message.priority.value,
                'recipient': message.recipient.value
            }
        )
        self._add_entry(entry)
    
    def log_event(self, level: LogLevel, source: str, message: str, metadata: Dict[str, Any] = None):
        """Log a general event"""
        entry = LogEntry(
            level=level,
            source=source,
            message=message,
            metadata=metadata or {}
        )
        self._add_entry(entry)
    
    def _add_entry(self, entry: LogEntry):
        """Add entry to log, maintaining max size"""
        self._entries.append(entry)
        if len(self._entries) > self._max_entries:
            self._entries.pop(0)
    
    def _get_log_level_for_message(self, message: InterAgentMessage) -> LogLevel:
        """Determine log level based on message priority"""
        priority_to_level = {
            Priority.CRITICAL: LogLevel.CRITICAL,
            Priority.HIGH: LogLevel.WARNING,
            Priority.MEDIUM: LogLevel.INFO,
            Priority.LOW: LogLevel.DEBUG
        }
        return priority_to_level.get(message.priority, LogLevel.INFO)
    
    def _format_message_for_log(self, message: InterAgentMessage) -> str:
        """Format message for log display"""
        if message.message_type == MessageType.SITUATION_UPDATE:
            situation = message.content.get('situation_description', 'Unknown situation')
            return f"Situation update: {situation[:50]}..."
        elif message.message_type == MessageType.DISPATCH_UPDATE:
            status = message.content.get('dispatch_status', 'Unknown status')
            eta = message.content.get('responder_eta', 'Unknown ETA')
            return f"Dispatch update: {status}, ETA {eta} min"
        elif message.message_type == MessageType.STATUS_UPDATE:
            status = message.content.get('status', 'Status update')
            return f"Status: {status}"
        elif message.message_type == MessageType.EMERGENCY_ESCALATION:
            reason = message.content.get('escalation_reason', 'Emergency escalation')
            return f"ESCALATION: {reason}"
        else:
            return f"{message.message_type.value}: {str(message.content)[:50]}..."
    
    def get_entries(self, limit: Optional[int] = None, level: Optional[LogLevel] = None) -> List[LogEntry]:
        """Get log entries, optionally filtered"""
        entries = self._entries
        
        if level:
            entries = [e for e in entries if e.level == level]
        
        if limit:
            entries = entries[-limit:]
            
        return entries
    
    def get_formatted_entries(self, limit: Optional[int] = None) -> List[str]:
        """Get formatted entries for display"""
        entries = self.get_entries(limit)
        return [entry.format_for_display() for entry in entries]
    
    def clear(self):
        """Clear all log entries"""
        self._entries.clear()


# Global event logger instance
_event_logger: Optional[EventLogger] = None

def get_event_logger() -> EventLogger:
    """Get the global event logger instance"""
    global _event_logger
    if _event_logger is None:
        _event_logger = EventLogger()
    return _event_logger 