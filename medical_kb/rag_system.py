"""
Fixed RAG system for medical knowledge with proper integration
"""
import json
import pickle
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class MedicalDocument:
    """Document in the medical knowledge base"""
    id: str
    condition: str
    patterns: List[str]
    content: str
    embedding: Optional[np.ndarray] = None

class MedicalRAGSystem:
    """
    🩺 MEDICAL RAG SYSTEM - Fixed and simplified
    """
    
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path(__file__).parent / "data"
        self.documents: List[MedicalDocument] = []
        self.embeddings: Optional[np.ndarray] = None
        self.embedding_model = None
        self.setup_complete = False
        
        # Load medical documents
        self._load_medical_documents()
        
        # Setup embedding model (optional)
        self._setup_embedding_model()
    
    def _load_medical_documents(self):
        """Load and process medical documents"""
        json_path = self.data_dir / "medical_intents.json"
        
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
            
            for intent in data.get("intents", []):
                if intent.get("responses") and intent["responses"][0].strip():
                    # Skip greeting/goodbye
                    if intent["tag"] in ["greeting", "goodbye"]:
                        continue
                        
                    # Create searchable content
                    content = f"Condition: {intent['tag']}\n"
                    content += f"Symptoms: {', '.join(intent['patterns'])}\n"
                    content += f"Treatment: {intent['responses'][0]}"
                    
                    doc = MedicalDocument(
                        id=intent["tag"].lower().replace(" ", "_"),
                        condition=intent["tag"],
                        patterns=intent["patterns"],
                        content=content
                    )
                    self.documents.append(doc)
            
            print(f"✅ Loaded {len(self.documents)} medical documents for RAG")
            
        except Exception as e:
            logger.error(f"Failed to load medical documents: {e}")
    
    def _setup_embedding_model(self):
        """Setup sentence transformer - with proper error handling"""
        try:
            from sentence_transformers import SentenceTransformer
            
            # Use a lightweight model
            model_name = "all-MiniLM-L6-v2"
            self.embedding_model = SentenceTransformer(model_name)
            print(f"✅ Loaded embedding model: {model_name}")
            
            # Generate embeddings
            self._generate_embeddings()
            
        except ImportError:
            print("⚠️  sentence-transformers not installed. Using keyword search only.")
            print("   Install with: pip install sentence-transformers")
        except Exception as e:
            print(f"⚠️  Embedding setup failed: {e}. Using keyword search only.")
    
    def _generate_embeddings(self):
        """Generate embeddings with better error handling"""
        if not self.embedding_model or not self.documents:
            return
        
        embeddings_path = self.data_dir / "rag_embeddings.pkl"
        
        # Try to load existing embeddings
        if embeddings_path.exists():
            try:
                with open(embeddings_path, 'rb') as f:
                    embedding_data = pickle.load(f)
                    self.embeddings = embedding_data["embeddings"]
                    
                    # Add embeddings to documents
                    for i, doc in enumerate(self.documents):
                        if i < len(self.embeddings):
                            doc.embedding = self.embeddings[i]
                    
                    print("✅ Loaded pre-computed RAG embeddings")
                    self.setup_complete = True
                    return
            except Exception as e:
                logger.debug(f"Could not load embeddings: {e}")
        
        # Generate new embeddings
        try:
            print("🔄 Generating embeddings...")
            texts = [doc.content for doc in self.documents]
            
            embeddings = self.embedding_model.encode(texts, show_progress_bar=False)
            self.embeddings = embeddings
            
            # Add embeddings to documents
            for i, doc in enumerate(self.documents):
                doc.embedding = embeddings[i]
            
            # Save embeddings
            embedding_data = {
                "embeddings": embeddings,
                "model_name": "all-MiniLM-L6-v2",  # Fixed model name
                "doc_count": len(self.documents)
            }
            
            with open(embeddings_path, 'wb') as f:
                pickle.dump(embedding_data, f)
            
            print("✅ Generated and saved RAG embeddings")
            self.setup_complete = True
            
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            print("⚠️  Embeddings failed, using keyword search only")
    
    def semantic_search(self, query: str, top_k: int = 3) -> List[Tuple[MedicalDocument, float]]:
        """Perform semantic search using embeddings"""
        if not self.embedding_model or not self.embeddings or not self.setup_complete:
            return self._keyword_search(query, top_k)
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query])
            
            # Calculate similarities
            similarities = np.dot(self.embeddings, query_embedding.T).flatten()
            
            # Get top-k results
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0.2:  # Minimum similarity threshold
                    results.append((self.documents[idx], float(similarities[idx])))
            
            return results
            
        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            return self._keyword_search(query, top_k)
    
    def _keyword_search(self, query: str, top_k: int = 3) -> List[Tuple[MedicalDocument, float]]:
        """Fallback keyword search"""
        query_words = set(query.lower().split())
        results = []
        
        for doc in self.documents:
            # Check condition name
            score = 0
            if any(word in doc.condition.lower() for word in query_words):
                score += 1.0
            
            # Check patterns
            for pattern in doc.patterns:
                pattern_words = set(pattern.lower().split())
                overlap = len(query_words.intersection(pattern_words))
                if overlap > 0:
                    score += overlap / len(query_words)
            
            if score > 0:
                results.append((doc, score))
        
        # Sort by score and return top-k
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    async def get_medical_advice(self, query: str) -> Dict[str, Any]:
        """
        Get medical advice using RAG approach
        """
        print(f"🧠 RAG Medical Search: {query}")
        
        try:
            # Step 1: Retrieve relevant documents
            retrieved_docs = self.semantic_search(query, top_k=2)
            
            if not retrieved_docs:
                return {
                    "status": "NO_RELEVANT_KNOWLEDGE",
                    "message": "No relevant medical knowledge found",
                    "query": query,
                    "method": "RAG_SEARCH"
                }
            
            # Step 2: Use the best match for advice
            best_doc, confidence = retrieved_docs[0]
            
            # Extract treatment from content
            treatment = ""
            for line in best_doc.content.split('\n'):
                if line.startswith("Treatment:"):
                    treatment = line.replace("Treatment:", "").strip()
                    break
            
            return {
                "status": "MEDICAL_ADVICE_FOUND",
                "condition": best_doc.condition,
                "confidence": confidence,
                "first_aid_instructions": treatment,
                "query": query,
                "method": "RAG_SEMANTIC_SEARCH" if self.setup_complete else "RAG_KEYWORD_SEARCH",
                "retrieved_conditions": [
                    {
                        "condition": doc.condition,
                        "confidence": float(score)
                    }
                    for doc, score in retrieved_docs
                ],
                "for_911_operator": f"First aid being provided for {best_doc.condition} based on medical protocols",
                "emergency_disclaimers": [
                    "This is first aid guidance only - not medical diagnosis",
                    "Call emergency services immediately for serious conditions",
                    "If condition worsens, seek immediate medical attention"
                ]
            }
            
        except Exception as e:
            return {
                "status": "RAG_ERROR",
                "error": str(e),
                "query": query
            }

# Global instance
_medical_rag = None

def get_medical_rag() -> MedicalRAGSystem:
    """Get global medical RAG system instance"""
    global _medical_rag
    if _medical_rag is None:
        _medical_rag = MedicalRAGSystem()
    return _medical_rag 