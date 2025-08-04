"""
Emergency tools for one-minute-agent.
Includes location services and medical advice systems.
"""

from .location import get_emergency_location
from .medical_advisor import get_first_aid_advice  # Traditional lookup
from .medical_rag_tool import get_rag_medical_advice  # RAG-powered
from nagents.base.tool_registry import ToolProvider

class VictimAssistantToolsProvider(ToolProvider):
    ...

tools = [
    get_emergency_location,
    get_first_aid_advice,
    get_rag_medical_advice
]

EMERGENCY_TOOLS = [
    get_emergency_location,
    get_first_aid_advice,
    get_rag_medical_advice
]

victim_assitant_tools = VictimAssistantToolsProvider().get_tools(tools=tools)

__all__ = [
    'get_emergency_location',
    'get_first_aid_advice', 
    'get_rag_medical_advice',
    'victim_assitant_tools'
]

