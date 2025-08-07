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
    """Check for Ollama in expected locations"""
    # On Hugging Face Spaces, Ollama should already be installed via Dockerfile
    ollama_paths = [
        Path("/opt/ollama/ollama"),  # Our Docker container location
        Path("/usr/local/bin/ollama"),  # Common system location
        Path.home() / "ollama"  # Legacy location in home dir
    ]
    
    # Check all possible paths
    for ollama_path in ollama_paths:
        print(f"🔍 Checking for Ollama at: {ollama_path}")
        
        if ollama_path.exists():
            file_size = ollama_path.stat().st_size
            print(f"✅ Ollama found at {ollama_path} ({file_size} bytes)")
            
            # Check if it's actually a binary (not an HTML error page)
            try:
                with open(ollama_path, 'rb') as f:
                    first_bytes = f.read(100)  # Read more bytes to better check the file
                    if b'<html' in first_bytes.lower() or b'<!doctype' in first_bytes.lower() or b'Not Found' in first_bytes:
                        print(f"❌ File at {ollama_path} is not a valid binary!")
                    else:
                        print(f"✅ File appears to be a binary at {ollama_path}")
                        
                        # Try to get version to verify it's working
                        try:
                            version_cmd = f"{ollama_path} --version"
                            version_result = subprocess.run(
                                version_cmd,
                                shell=True,
                                capture_output=True,
                                text=True,
                                timeout=5
                            )
                            if version_result.returncode == 0:
                                print(f"✅ Ollama version: {version_result.stdout.strip()}")
                                os.environ['OLLAMA_PATH'] = str(ollama_path)  # Set for later use
                                return True
                            else:
                                print(f"⚠️ Failed to get Ollama version: {version_result.stderr}")
                        except Exception as e:
                            print(f"⚠️ Error checking Ollama version: {e}")
            except Exception as e:
                print(f"❌ Error reading file: {e}")
    
    print("❌ No valid Ollama installation found")
    return False

def start_ollama_service():
    """Start Ollama service in background thread"""
    def ollama_service_thread():
        # Get the ollama path from environment or use default
        ollama_path = os.environ.get('OLLAMA_PATH', '/opt/ollama/ollama')
        
        try:
            print(f"🔧 Starting Ollama service: {ollama_path} serve")
            # Set host explicitly to make sure it's accessible from outside the container
            serve_cmd = f"{ollama_path} serve"
            
            # Use longer timeout and better error handling
            result = subprocess.run(
                serve_cmd, 
                shell=True, 
                capture_output=True, 
                text=True
            )
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
    
    # Give Ollama more time to start up (especially on first run)
    print("⏳ Giving Ollama serve 30 seconds to start...")
    time.sleep(30)
    
    # Test if Ollama server is responding by checking its API
    try:
        health_check = subprocess.run(
            "curl -s -m 5 http://localhost:11434/api/version",
            shell=True,
            capture_output=True,
            text=True
        )
        if health_check.returncode == 0 and health_check.stdout:
            print(f"✅ Ollama API is responding: {health_check.stdout.strip()}")
        else:
            print("⚠️ Ollama API not responding to health check")
    except Exception as e:
        print(f"⚠️ Ollama health check error: {e}")
    
    return service_thread

def pull_model(model_name="gemma3n:e2b"):
    """Pull the specified model"""
    # Get the ollama path from environment or use default
    ollama_path = os.environ.get('OLLAMA_PATH', '/opt/ollama/ollama')
    
    print(f"📦 Pulling model: {model_name}")
    try:
        # Check if the model already exists
        list_cmd = f"{ollama_path} list"
        list_result = subprocess.run(
            list_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if model_name in list_result.stdout:
            print(f"✅ Model {model_name} is already available")
            return True
        
        # Pull the model with increased timeout
        pull_cmd = f"{ollama_path} pull {model_name}"
        print(f"🔧 Running: {pull_cmd}")
        
        result = subprocess.run(
            pull_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=1200  # 20 minute timeout for model download (HF Spaces has limited bandwidth)
        )
        
        print(f"📦 Model pull result: return code {result.returncode}")
        if result.stdout:
            print(f"📦 Model pull stdout: {result.stdout[:500]}..." if len(result.stdout) > 500 else f"📦 Model pull stdout: {result.stdout}")
        if result.stderr:
            print(f"📦 Model pull stderr: {result.stderr[:500]}..." if len(result.stderr) > 500 else f"📦 Model pull stderr: {result.stderr}")
        
        if result.returncode == 0:
            print(f"✅ Model {model_name} pulled successfully")
            return True
        else:
            print(f"❌ Failed to pull model: {result.stderr[:200]}" if result.stderr else "❌ Failed to pull model with unknown error")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ Model pull timed out after 20 minutes. This is common on Hugging Face Spaces due to bandwidth limitations.")
        print("Continuing anyway, as the model might be partially downloaded and usable...")
        # Don't return False immediately - try using the model anyway
        return True
    except Exception as e:
        print(f"❌ Error pulling model: {e}")
        return False

def test_ollama_connection(model_name="gemma3n:e2b"):
    """Test if Ollama is working with the model"""
    try:
        print(f"🧪 Testing Ollama connection with model: {model_name}")
        import ollama
        
        # First try to list models to check basic connectivity
        try:
            models = ollama.list()
            print(f"✅ Ollama API connection successful, models: {models}")
        except Exception as e:
            print(f"⚠️ Ollama list models failed: {e}")
            
        # Set longer timeout for chat test
        # Specify the API host explicitly to match our Docker environment
        import os
        host = os.environ.get('OLLAMA_HOST', '127.0.0.1:11434')
        
        # Configure the client to use our host
        ollama.HOST = f"http://{host}"
        print(f"📡 Using Ollama API at: {ollama.HOST}")
        
        # Test with a simple message and longer timeout
        try:
            print("🧪 Testing chat with a simple message...")
            response = ollama.chat(
                model=model_name,
                messages=[{"role": "user", "content": "Hello, please respond with a single word."}],
                options={"temperature": 0}
            )
            
            print(f"✅ Ollama connection test successful: {response}")
            return True
        except Exception as e:
            print(f"❌ Ollama chat test failed: {e}")
            # Continue anyway and don't fail completely
            return False
            
    except Exception as e:
        print(f"❌ Ollama connection test failed: {e}")
        # Import error or other - might still work with API directly
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