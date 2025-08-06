"""
Ollama setup and initialization for Hugging Face Spaces
"""
import os
import threading
import time
import subprocess
import sys
from pathlib import Path

def setup_ollama():
    """Download and setup Ollama if not already available"""
    ollama_path = Path.home() / "ollama"
    
    if not ollama_path.exists():
        print("📥 Downloading Ollama...")
        try:
            result = subprocess.run(
                f"curl -L https://ollama.com/download/ollama-linux-amd64 -o {ollama_path}",
                shell=True,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                os.chmod(ollama_path, 0o755)
                print("✅ Ollama downloaded successfully")
                return True
            else:
                print(f"❌ Failed to download Ollama: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Error downloading Ollama: {e}")
            return False
    else:
        print("✅ Ollama already available")
        return True

def start_ollama_service():
    """Start Ollama service in background thread"""
    def ollama_service_thread():
        ollama_path = Path.home() / "ollama"
        try:
            print("🔧 Starting Ollama service...")
            subprocess.run(f"{ollama_path} serve", shell=True)
        except Exception as e:
            print(f"❌ Ollama service error: {e}")
    
    service_thread = threading.Thread(target=ollama_service_thread, daemon=True)
    service_thread.start()
    
    print("⏳ Giving Ollama serve a moment to start...")
    time.sleep(10)
    
    return service_thread

def pull_model(model_name="gemma3n:e2b"):
    """Pull the specified model"""
    ollama_path = Path.home() / "ollama"
    
    print(f"📦 Pulling model: {model_name}")
    try:
        result = subprocess.run(
            f"{ollama_path} pull {model_name}",
            shell=True,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode == 0:
            print(f"✅ Model {model_name} pulled successfully")
            return True
        else:
            print(f"❌ Failed to pull model: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ Model pull timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"❌ Error pulling model: {e}")
        return False

def test_ollama_connection(model_name="gemma3n:e2b"):
    """Test if Ollama is working with the model"""
    try:
        import ollama
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": "Hello"}]
        )
        print("✅ Ollama connection test successful")
        return True
    except Exception as e:
        print(f"❌ Ollama connection test failed: {e}")
        return False

def initialize_ollama(model_name="gemma3n:e2b"):
    """Complete Ollama initialization process"""
    print("🚀 Initializing Ollama...")
    
    # Step 1: Setup/download Ollama
    if not setup_ollama():
        return False
    
    # Step 2: Start service
    start_ollama_service()
    
    # Step 3: Pull model
    if not pull_model(model_name):
        print("⚠️ Model pull failed, but continuing...")
    
    # Step 4: Test connection
    if test_ollama_connection(model_name):
        print("🎉 Ollama initialization complete!")
        return True
    else:
        print("⚠️ Ollama connection test failed")
        return False

if __name__ == "__main__":
    initialize_ollama() 