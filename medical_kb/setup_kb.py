#!/usr/bin/env python3
"""
Setup script for medical knowledge base.
Moves data and optionally creates embeddings.
"""
import json
import shutil
from pathlib import Path

def setup_medical_kb():
    """Setup medical knowledge base"""
    print("🩺 Setting up Medical Knowledge Base...")
    
    # Create directories
    kb_dir = Path(__file__).parent
    data_dir = kb_dir / "data"
    data_dir.mkdir(exist_ok=True)
    
    # Move intents.json to medical_kb/data/
    old_path = kb_dir.parent / "tools" / "intents.json"
    new_path = data_dir / "medical_intents.json"
    
    if old_path.exists() and not new_path.exists():
        shutil.copy2(old_path, new_path)
        print(f"✅ Moved medical data to {new_path}")
    
    # Validate data
    try:
        with open(new_path, 'r') as f:
            data = json.load(f)
        
        intent_count = len(data.get("intents", []))
        valid_intents = sum(1 for i in data["intents"] if i.get("responses") and i["responses"][0].strip())
        
        print(f"✅ Validated medical data: {valid_intents}/{intent_count} usable entries")
        
    except Exception as e:
        print(f"❌ Data validation failed: {e}")
        return False
    
    print("✅ Medical Knowledge Base setup complete!")
    return True

if __name__ == "__main__":
    setup_medical_kb() 