"""
FastAPI backend for React Emergency Response App
Integrates with Python agents and provides WebSocket support
"""
import sys
from pathlib import Path

# Add the project path for agent imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import json
from datetime import datetime
import uuid

from nagents import OllamaProvider
from one_minute_agent.agents import create_agent
from one_minute_agent.communication import (
    get_coordination_system, get_message_bus, get_event_logger,
    MessageType, Priority, AgentRole
)

app = FastAPI(title="Emergency Response API")

# CORS middleware for React development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite and CRA defaults
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve React build files (for production)
app.mount("/static", StaticFiles(directory="dist"), name="static")

# Global state
agents = {}
communication_system = None
connected_clients: List[WebSocket] = []

class ChatMessage(BaseModel):
    text: str
    agent_type: str  # "victim-assistant" or "operator"

class ChatResponse(BaseModel):
    id: str
    text: str
    sender: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None

@app.on_event("startup")
async def startup_event():
    """Initialize agents on startup"""
    global agents, communication_system
    
    try:
        # Initialize model provider
        model_provider = OllamaProvider("gemma3n:e2b")
        
        # Initialize communication system
        coordination_system = get_coordination_system()
        message_bus = get_message_bus()
        event_logger = get_event_logger()
        message_bus.clear_history()
        
        communication_system = {
            'coordination': coordination_system,
            'message_bus': message_bus,
            'event_logger': event_logger
        }
        
        # Create agents
        agents['victim-assistant'] = create_agent(
            agent_type="victim-assistant",
            model_provider=model_provider,
            max_iterations=3,
            show_thinking=False,
            enable_communication=True
        )
        
        agents['operator'] = create_agent(
            agent_type="operator", 
            model_provider=model_provider,
            max_iterations=3,
            show_thinking=False,
            enable_communication=True
        )
        
        print("✅ Agents initialized successfully")
        
    except Exception as e:
        print(f"❌ Failed to initialize agents: {e}")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    connected_clients.append(websocket)
    
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            # Echo back for now - can be extended for real-time features
            await websocket.send_text(f"Echo: {data}")
            
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

async def broadcast_to_clients(message: Dict[str, Any]):
    """Broadcast message to all connected WebSocket clients"""
    if connected_clients:
        message_json = json.dumps(message, default=str)
        disconnected = []
        
        for client in connected_clients:
            try:
                await client.send_text(message_json)
            except:
                disconnected.append(client)
        
        # Remove disconnected clients
        for client in disconnected:
            connected_clients.remove(client)

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_agent(message: ChatMessage):
    """Send message to agent and get response"""
    try:
        agent = agents.get(message.agent_type)
        if not agent:
            raise HTTPException(status_code=400, detail=f"Agent type '{message.agent_type}' not found")
        
        # Get agent response
        result = agent.chat(message.text)
        
        response = ChatResponse(
            id=str(uuid.uuid4()),
            text=result.content,
            sender="assistant",
            timestamp=datetime.now(),
            metadata={
                "tools_executed": len(result.tools_executed) if result.tools_executed else 0,
                "agent_type": message.agent_type
            }
        )
        
        # Broadcast to WebSocket clients for real-time updates
        await broadcast_to_clients({
            "type": "agent_response",
            "agent_type": message.agent_type,
            "response": response.dict()
        })
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

@app.get("/api/inter-agent-log")
async def get_inter_agent_log():
    """Get inter-agent communication log"""
    if not communication_system:
        return {"messages": []}
    
    try:
        message_bus = communication_system['message_bus']
        messages = message_bus.get_message_history()
        
        formatted_messages = []
        for msg in messages[-50:]:  # Last 50 messages
            formatted_messages.append({
                "id": str(uuid.uuid4()),
                "timestamp": msg.timestamp.isoformat(),
                "type": msg.message_type.value,
                "sender": msg.sender.value if hasattr(msg.sender, 'value') else str(msg.sender),
                "recipient": msg.recipient.value if hasattr(msg.recipient, 'value') else str(msg.recipient),
                "content": msg.content,
                "priority": msg.priority.value if hasattr(msg.priority, 'value') else str(msg.priority)
            })
        
        return {"messages": formatted_messages}
        
    except Exception as e:
        return {"error": str(e), "messages": []}

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agents_initialized": bool(agents),
        "communication_system": bool(communication_system),
        "connected_clients": len(connected_clients)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 