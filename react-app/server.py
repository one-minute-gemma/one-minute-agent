"""
Unified FastAPI server for React + Agent integration
Optimized for Hugging Face Spaces deployment
"""
import sys
import os
from pathlib import Path

# Add project paths
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / "one_minute_agent"))
sys.path.append(str(Path(__file__).parent / "nagents"))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import json
from datetime import datetime
import uuid
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Emergency Response System")

# Serve React static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global state for demo
connected_clients: List[WebSocket] = []
agents_initialized = False

class ChatMessage(BaseModel):
    text: str
    agent_type: str  # "victim-assistant" or "operator"

class ChatResponse(BaseModel):
    id: str
    text: str
    sender: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None

# Mock agent responses for demo (replace with real agents when Ollama is available)
MOCK_RESPONSES = {
    "victim-assistant": [
        "I understand. Help is on the way. Can you tell me if you're in a safe location right now?",
        "Thank you for that information. Emergency responders are 3 minutes away. Stay with me.",
        "You're doing great. Keep talking to me while we wait for help to arrive.",
        "I've updated the emergency team with your information. They'll be there soon.",
        "Please stay calm. Can you tell me if anyone else is with you?",
        "That's very helpful information. I'm passing this to the responders right now.",
        "You're being very brave. Help will be there in just a few minutes.",
    ],
    "operator": [
        "Unit 23 dispatched to your location. ETA 4 minutes.",
        "Fire department and paramedics en route. Confirmed emergency at location.",
        "Additional units being dispatched. Please maintain communication with victim.",
        "Responders are 2 minutes out. Preparing for arrival.",
        "Emergency team has been briefed on situation. Standing by for updates.",
        "All units converging on location. ETA reduced to 90 seconds.",
    ]
}

def initialize_agents():
    """Initialize agents - mock for demo, real implementation when Ollama available"""
    global agents_initialized
    try:
        # Try to initialize real agents
        from nagents import OllamaProvider
        from one_minute_agent.agents import create_agent
        
        model_provider = OllamaProvider("gemma3n:e2b")
        # Real agent initialization would go here
        agents_initialized = True
        logger.info("✅ Real agents initialized")
        return True
        
    except Exception as e:
        logger.warning(f"⚠️ Real agents not available, using mock responses: {e}")
        agents_initialized = True  # Use mock mode
        return False

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    initialize_agents()

@app.get("/")
async def serve_react_app():
    """Serve React app"""
    return FileResponse("static/index.html")

@app.get("/{path:path}")
async def serve_react_routes(path: str):
    """Serve React app for all routes (SPA routing)"""
    file_path = Path("static") / path
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    return FileResponse("static/index.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time updates"""
    await websocket.accept()
    connected_clients.append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            # Echo for now - can be extended
            await websocket.send_text(f"Connected: {len(connected_clients)} clients")
            
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

async def broadcast_to_clients(message: Dict[str, Any]):
    """Broadcast to WebSocket clients"""
    if connected_clients:
        message_json = json.dumps(message, default=str)
        disconnected = []
        
        for client in connected_clients:
            try:
                await client.send_text(message_json)
            except:
                disconnected.append(client)
        
        for client in disconnected:
            connected_clients.remove(client)

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_agent(message: ChatMessage):
    """Chat endpoint - uses mock responses for demo"""
    try:
        # Simulate processing delay
        await asyncio.sleep(0.5 + (0.5 * len(message.text) / 100))
        
        # Get mock response
        responses = MOCK_RESPONSES.get(message.agent_type, ["I'm here to help."])
        response_text = responses[hash(message.text) % len(responses)]
        
        response = ChatResponse(
            id=str(uuid.uuid4()),
            text=response_text,
            sender="assistant",
            timestamp=datetime.now(),
            metadata={
                "agent_type": message.agent_type,
                "mock_mode": True
            }
        )
        
        # Broadcast to WebSocket clients
        await broadcast_to_clients({
            "type": "agent_response",
            "agent_type": message.agent_type,
            "response": response.dict()
        })
        
        return response
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@app.get("/api/inter-agent-log")
async def get_inter_agent_log():
    """Mock inter-agent log for demo"""
    mock_messages = [
        {
            "id": str(uuid.uuid4()),
            "timestamp": (datetime.now()).isoformat(),
            "type": "SITUATION_UPDATE",
            "sender": "VICTIM_ASSISTANT",
            "recipient": "OPERATOR",
            "content": {"situation": "Fire emergency reported", "priority": "HIGH"},
            "priority": "HIGH"
        },
        {
            "id": str(uuid.uuid4()),
            "timestamp": (datetime.now()).isoformat(),
            "type": "DISPATCH_UPDATE", 
            "sender": "OPERATOR",
            "recipient": "VICTIM_ASSISTANT",
            "content": {"status": "Units dispatched", "eta": 4},
            "priority": "HIGH"
        }
    ]
    
    return {"messages": mock_messages}

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agents_initialized": agents_initialized,
        "connected_clients": len(connected_clients),
        "mode": "production" if agents_initialized else "demo"
    }

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment (Hugging Face Spaces uses 7860)
    port = int(os.environ.get("PORT", 7860))
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info"
    ) 