"""
Victim Assistant Agent Tools - for direct victim assistance.
Uses existing RAG medical tools and first aid guidance systems.
"""

# Import existing medical and RAG tools that help victims directly
import sys
import os
# Add the project root to the path so we can import tools
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../..'))

from tools.medical_advisor import get_first_aid_advice  # Traditional first aid lookup
from tools.medical_rag_tool import get_rag_medical_advice  # RAG-powered medical advice
from tools.location import get_emergency_location  # Shared location tool

from nagents.base.tool_registry import ToolProvider

class VictimAssistantToolsProvider(ToolProvider):
    ...

tools = [
    get_emergency_location,
    get_first_aid_advice,
    get_rag_medical_advice
]
victim_assitant_tools = VictimAssistantToolsProvider().get_tools(tools=tools)