"""
Emergency tools for one-minute-agent.
Production-ready location services for crisis situations.
"""

from .location import get_emergency_location

# Main emergency tools
__all__ = ['get_emergency_location']

# Tool registry for nagents framework
EMERGENCY_TOOLS = [get_emergency_location]

