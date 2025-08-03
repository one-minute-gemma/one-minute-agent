"""
RAG-based medical advisor using semantic search + LLM generation
"""
from typing import Dict, Any
import sys
from pathlib import Path

# Add medical_kb to path
sys.path.append(str(Path(__file__).parent.parent))

from medical_kb.rag_system import get_medical_rag

async def get_rag_medical_advice(symptoms: str) -> Dict[str, Any]:
    """
    🧠 Get RAG-generated medical advice using semantic search + LLM
    
    This uses true RAG: retrieves relevant medical knowledge using embeddings,
    then generates personalized advice using a language model.
    
    Args:
        symptoms: Description of symptoms or medical situation
        
    Returns:
        Dict with generated advice, retrieved context, and relevance scores
    """
    try:
        rag_system = get_medical_rag()
        return await rag_system.get_rag_medical_advice(symptoms)
        
    except Exception as e:
        return {
            "status": "RAG_SYSTEM_ERROR",
            "error": str(e),
            "fallback": "Use traditional medical lookup system"
        }

# Export for comparison
__all__ = ['get_rag_medical_advice'] 