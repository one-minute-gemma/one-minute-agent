"""
RAG-based medical tool for one-minute-agent integration
"""
from typing import Dict, Any
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from medical_kb.rag_system import get_medical_rag

async def get_rag_medical_advice(symptoms: str) -> Dict[str, Any]:
    """
    🧠 RAG-powered medical advice tool for emergency agents.
    
    Uses semantic search to find relevant medical knowledge and provides
    contextual first aid instructions for emergency situations.
    
    Args:
        symptoms: Description of symptoms, injury, or medical condition
        
    Returns:
        Dict containing RAG-generated advice, confidence scores, and emergency guidance
    """
    print(f"🩺 RAG Medical Tool: Analyzing - {symptoms}")
    
    try:
        rag_system = get_medical_rag()
        advice = await rag_system.get_medical_advice(symptoms)
        
        if advice["status"] == "MEDICAL_ADVICE_FOUND":
            print(f"✅ RAG found advice for: {advice['condition']}")
            print(f"📊 Confidence: {advice['confidence']:.2f}")
            
        return advice
        
    except Exception as e:
        return {
            "status": "RAG_SYSTEM_ERROR",
            "error": str(e),
            "fallback_advice": "Monitor patient and ensure airway is clear",
            "emergency_note": "Continue with standard emergency procedures"
        }

# Export for agent use
__all__ = ['get_rag_medical_advice']