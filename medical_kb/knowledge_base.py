"""
Offline Medical Knowledge Base with RAG capabilities.
Uses local embeddings and fuzzy matching for reliable emergency information.
"""
import json
import pickle
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import re

logger = logging.getLogger(__name__)

@dataclass
class MedicalKnowledge:
    """Container for medical knowledge entries"""
    tag: str
    patterns: List[str]
    response: str
    confidence: float = 0.0

class MedicalKnowledgeBase:
    """
    🩺 OFFLINE MEDICAL KNOWLEDGE BASE
    
    Provides first aid information through multiple retrieval methods:
    1. Exact keyword matching (fastest)
    2. Fuzzy pattern matching (handles typos)  
    3. Semantic similarity (handles different phrasings)
    """
    
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path(__file__).parent / "data"
        self.knowledge_entries: List[MedicalKnowledge] = []
        self.embeddings = None
        self.embedding_model = None
        self.setup_complete = False
        
        # Load knowledge base
        self._load_knowledge_base()
        
        # Try to load embeddings (optional for basic functionality)
        self._load_embeddings()
    
    def _load_knowledge_base(self):
        """Load medical knowledge from JSON file"""
        json_path = self.data_dir / "medical_intents.json"
        
        if not json_path.exists():
            # Fallback to old location
            json_path = Path(__file__).parent.parent / "tools" / "intents.json"
        
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
            
            for intent in data.get("intents", []):
                if intent.get("responses") and intent["responses"][0].strip():
                    self.knowledge_entries.append(MedicalKnowledge(
                        tag=intent["tag"],
                        patterns=intent["patterns"],
                        response=intent["responses"][0]
                    ))
            
            print(f"✅ Loaded {len(self.knowledge_entries)} medical knowledge entries")
            self.setup_complete = True
            
        except Exception as e:
            logger.error(f"Failed to load medical knowledge: {e}")
            self.knowledge_entries = []
    
    def _load_embeddings(self):
        """Load pre-computed embeddings if available"""
        embeddings_path = self.data_dir / "embeddings.pkl"
        
        if embeddings_path.exists():
            try:
                with open(embeddings_path, 'rb') as f:
                    embedding_data = pickle.load(f)
                    self.embeddings = embedding_data.get("embeddings")
                    self.embedding_model_name = embedding_data.get("model_name")
                
                print("✅ Loaded pre-computed medical embeddings")
                return True
            except Exception as e:
                logger.debug(f"Could not load embeddings: {e}")
        
        return False
    
    def search_medical_info(self, query: str, max_results: int = 3) -> List[MedicalKnowledge]:
        """
        🔍 Search for medical information using multiple methods
        
        Args:
            query: User's medical question/symptom
            max_results: Maximum number of results to return
            
        Returns:
            List of MedicalKnowledge entries ranked by relevance
        """
        if not self.knowledge_entries:
            return []
        
        results = []
        query_lower = query.lower()
        
        # Method 1: Exact keyword matching (highest priority)
        exact_matches = self._exact_keyword_search(query_lower)
        results.extend(exact_matches)
        
        # Method 2: Fuzzy pattern matching
        if len(results) < max_results:
            fuzzy_matches = self._fuzzy_pattern_search(query_lower)
            results.extend([r for r in fuzzy_matches if r not in results])
        
        # Method 3: Semantic similarity (if embeddings available)
        if len(results) < max_results and self.embeddings:
            semantic_matches = self._semantic_search(query)
            results.extend([r for r in semantic_matches if r not in results])
        
        # Remove duplicates while preserving order and limit results
        unique_results = []
        seen_tags = set()
        for result in results:
            if result.tag not in seen_tags:
                unique_results.append(result)
                seen_tags.add(result.tag)
                if len(unique_results) >= max_results:
                    break
        
        return unique_results
    
    def _exact_keyword_search(self, query: str) -> List[MedicalKnowledge]:
        """Find entries with exact keyword matches"""
        matches = []
        
        for entry in self.knowledge_entries:
            # Check tag
            if entry.tag.lower() in query or query in entry.tag.lower():
                entry.confidence = 1.0
                matches.append(entry)
                continue
            
            # Check patterns
            for pattern in entry.patterns:
                if pattern.lower() in query or query in pattern.lower():
                    entry.confidence = 0.9
                    matches.append(entry)
                    break
        
        return sorted(matches, key=lambda x: x.confidence, reverse=True)
    
    def _fuzzy_pattern_search(self, query: str) -> List[MedicalKnowledge]:
        """Find entries using fuzzy string matching"""
        matches = []
        
        # Simple fuzzy matching using word overlap
        query_words = set(re.findall(r'\w+', query.lower()))
        
        if not query_words:
            return matches
        
        for entry in self.knowledge_entries:
            max_overlap = 0
            
            # Check against tag
            tag_words = set(re.findall(r'\w+', entry.tag.lower()))
            overlap = len(query_words.intersection(tag_words))
            max_overlap = max(max_overlap, overlap)
            
            # Check against patterns
            for pattern in entry.patterns:
                pattern_words = set(re.findall(r'\w+', pattern.lower()))
                overlap = len(query_words.intersection(pattern_words))
                max_overlap = max(max_overlap, overlap)
            
            # Include if significant word overlap
            if max_overlap >= 1:
                entry.confidence = min(0.8, max_overlap / len(query_words))
                matches.append(entry)
        
        return sorted(matches, key=lambda x: x.confidence, reverse=True)
    
    def _semantic_search(self, query: str) -> List[MedicalKnowledge]:
        """Semantic search using embeddings (if available)"""
        # This would use sentence-transformers for semantic similarity
        # For now, return empty list as embeddings are optional
        return []
    
    def get_emergency_advice(self, symptoms: str) -> Dict[str, Any]:
        """
        🚨 Get emergency first aid advice for symptoms
        
        Args:
            symptoms: Description of symptoms or medical situation
            
        Returns:
            Dict with advice, confidence, and emergency guidance
        """
        print(f"🩺 Searching medical knowledge for: {symptoms}")
        
        if not self.setup_complete:
            return {
                "status": "KNOWLEDGE_BASE_ERROR",
                "message": "Medical knowledge base not available",
                "emergency_note": "Proceed with standard emergency protocols"
            }
        
        results = self.search_medical_info(symptoms, max_results=2)
        
        if not results:
            return {
                "status": "NO_MATCH_FOUND",
                "message": f"No specific first aid information found for: {symptoms}",
                "general_advice": "Monitor vital signs and call emergency services if condition worsens",
                "emergency_note": "When in doubt, seek immediate medical attention"
            }
        
        primary_result = results[0]
        
        response = {
            "status": "FIRST_AID_ADVICE_FOUND",
            "condition": primary_result.tag,
            "confidence": primary_result.confidence,
            "first_aid_instructions": primary_result.response,
            "source": "offline_medical_kb",
            "timestamp": self._get_timestamp()
        }
        
        # Add alternative suggestions if available
        if len(results) > 1:
            response["alternative_conditions"] = [
                {
                    "condition": r.tag,
                    "confidence": r.confidence,
                    "instructions": r.response[:100] + "..."
                }
                for r in results[1:]
            ]
        
        # Add emergency disclaimers
        response["emergency_disclaimers"] = [
            "This is first aid guidance only - not medical diagnosis",
            "Call emergency services immediately for serious conditions",
            "If condition worsens, seek immediate medical attention"
        ]
        
        print(f"✅ Found first aid advice for: {primary_result.tag}")
        return response
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_available_conditions(self) -> List[str]:
        """Get list of all available medical conditions"""
        return [entry.tag for entry in self.knowledge_entries]

# Global instance for easy access
_medical_kb = None

def get_medical_kb() -> MedicalKnowledgeBase:
    """Get global medical knowledge base instance"""
    global _medical_kb
    if _medical_kb is None:
        _medical_kb = MedicalKnowledgeBase()
    return _medical_kb