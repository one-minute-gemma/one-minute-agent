"""
Medical advisor tool that provides first aid guidance using the knowledge base.
"""
from typing import Dict, Any
import sys
from pathlib import Path

# Add medical_kb to path
sys.path.append(str(Path(__file__).parent.parent))

from medical_kb import get_medical_kb

async def get_first_aid_advice(symptoms: str) -> Dict[str, Any]:
    """
    🩺 Get first aid advice for medical symptoms or conditions.
    
    This tool provides evidence-based first aid instructions that can be
    communicated to the user or bystanders while waiting for emergency services.
    
    Args:
        symptoms: Description of symptoms, injury, or medical condition
        
    Returns:
        Dict containing first aid instructions, confidence level, and safety notes
    """
    print(f"🩺 Medical Advisor: Analyzing symptoms - {symptoms}")
    
    try:
        medical_kb = get_medical_kb()
        advice = medical_kb.get_emergency_advice(symptoms)
        
        if advice["status"] == "FIRST_AID_ADVICE_FOUND":
            print(f"✅ First aid advice found for: {advice['condition']}")
            print(f"📋 Confidence: {advice['confidence']:.1%}")
            
            # Format for emergency communication
            advice["for_911_operator"] = f"First aid being provided for {advice['condition']} based on medical protocols"
            advice["for_bystanders"] = advice["first_aid_instructions"]
            
        return advice
        
    except Exception as e:
        return {
            "status": "MEDICAL_ADVISOR_ERROR",
            "error": str(e),
            "fallback_advice": "Monitor patient, ensure airway is clear, and wait for emergency services",
            "emergency_note": "Continue with standard emergency procedures"
        }

def search_medical_conditions(query: str) -> Dict[str, Any]:
    """
    🔍 Search available medical conditions in knowledge base.
    
    Args:
        query: Search term for medical conditions
        
    Returns:
        Dict with matching conditions and their basic info
    """
    try:
        medical_kb = get_medical_kb()
        results = medical_kb.search_medical_info(query, max_results=5)
        
        return {
            "status": "SEARCH_COMPLETE",
            "query": query,
            "matches": [
                {
                    "condition": r.tag,
                    "confidence": r.confidence,
                    "sample_patterns": r.patterns[:2]  # Show first 2 patterns
                }
                for r in results
            ],
            "total_available": len(medical_kb.get_available_conditions())
        }
        
    except Exception as e:
        return {
            "status": "SEARCH_ERROR",
            "error": str(e)
        }

# Export for agent use
__all__ = ['get_first_aid_advice', 'search_medical_conditions'] 