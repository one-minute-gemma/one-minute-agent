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
    
    print(f"🔍 Checking for Ollama at: {ollama_path}")
    
    if not ollama_path.exists():
        print("📥 Downloading Ollama...")
        try:
            download_cmd = f"curl -L https://ollama.com/download/ollama-linux-amd64 -o {ollama_path}"
            print(f"🔧 Running: {download_cmd}")
            
            result = subprocess.run(
                download_cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            print(f"📦 Download result: return code {result.returncode}")
            if result.stdout:
                print(f"📦 Download stdout: {result.stdout}")
            if result.stderr:
                print(f"📦 Download stderr: {result.stderr}")
            
            if result.returncode == 0:
                print(f"🔧 Setting permissions on {ollama_path}")
                os.chmod(ollama_path, 0o755)
                
                # Verify the download
                if ollama_path.exists():
                    file_size = ollama_path.stat().st_size
                    print(f"✅ Ollama downloaded successfully ({file_size} bytes)")
                    
                    # Check if it's actually a binary (not an HTML error page)
                    with open(ollama_path, 'rb') as f:
                        first_bytes = f.read(10)
                        if b'<html' in first_bytes.lower() or b'<!doctype' in first_bytes.lower():
                            print("❌ Downloaded file appears to be HTML, not a binary!")
                            return False
                        else:
                            print(f"✅ File appears to be a binary (first bytes: {first_bytes})")
                    
                    return True
                else:
                    print("❌ File not found after download")
                    return False
            else:
                print(f"❌ Failed to download Ollama: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("⏰ Download timed out after 2 minutes")
            return False
        except Exception as e:
            print(f"❌ Error downloading Ollama: {e}")
            return False
    else:
        file_size = ollama_path.stat().st_size
        print(f"✅ Ollama already available ({file_size} bytes)")
        return True

def start_ollama_service():
    """Start Ollama service in background thread"""
    def ollama_service_thread():
        ollama_path = Path.home() / "ollama"
        try:
            print(f"🔧 Starting Ollama service: {ollama_path} serve")
            result = subprocess.run(f"{ollama_path} serve", shell=True, capture_output=True, text=True)
            print(f"🔧 Ollama serve result: {result.returncode}")
            if result.stdout:
                print(f"🔧 Ollama serve stdout: {result.stdout}")
            if result.stderr:
                print(f"🔧 Ollama serve stderr: {result.stderr}")
        except Exception as e:
            print(f"❌ Ollama service error: {e}")
    
    print("🚀 Starting Ollama service thread...")
    service_thread = threading.Thread(target=ollama_service_thread, daemon=True)
    service_thread.start()
    
    print("⏳ Giving Ollama serve 15 seconds to start...")
    time.sleep(15)
    
    return service_thread

def pull_model(model_name="gemma3n:e2b"):
    """Pull the specified model"""
    ollama_path = Path.home() / "ollama"
    
    print(f"📦 Pulling model: {model_name}")
    try:
        pull_cmd = f"{ollama_path} pull {model_name}"
        print(f"🔧 Running: {pull_cmd}")
        
        result = subprocess.run(
            pull_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout for model download
        )
        
        print(f"📦 Model pull result: return code {result.returncode}")
        if result.stdout:
            print(f"📦 Model pull stdout: {result.stdout}")
        if result.stderr:
            print(f"📦 Model pull stderr: {result.stderr}")
        
        if result.returncode == 0:
            print(f"✅ Model {model_name} pulled successfully")
            return True
        else:
            print(f"❌ Failed to pull model: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ Model pull timed out after 10 minutes")
        return False
    except Exception as e:
        print(f"❌ Error pulling model: {e}")
        return False

def test_ollama_connection(model_name="gemma3n:e2b"):
    """Test if Ollama is working with the model"""
    try:
        print(f"🧪 Testing Ollama connection with model: {model_name}")
        import ollama
        
        response = ollama.chat(
            model=model_name,
            messages=[{"role": "user", "content": "Hello"}]
        )
        
        print(f"✅ Ollama connection test successful: {response}")
        return True
    except Exception as e:
        print(f"❌ Ollama connection test failed: {e}")
        return False

def initialize_ollama(model_name="gemma3n:e2b"):
    """Complete Ollama initialization process"""
    print("🚀 Starting Ollama initialization...")
    
    # Step 1: Setup/download Ollama
    print("📥 Step 1: Setting up Ollama...")
    if not setup_ollama():
        print("❌ Ollama setup failed")
        return False
    
    # Step 2: Start service
    print("🔧 Step 2: Starting Ollama service...")
    start_ollama_service()
    
    # Step 3: Pull model
    print("📦 Step 3: Pulling model...")
    if not pull_model(model_name):
        print("⚠️ Model pull failed, but continuing...")
    
    # Step 4: Test connection
    print("🧪 Step 4: Testing connection...")
    if test_ollama_connection(model_name):
        print("🎉 Ollama initialization complete!")
        return True
    else:
        print("⚠️ Ollama connection test failed")
        return False

if __name__ == "__main__":
    initialize_ollama() 