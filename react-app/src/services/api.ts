// API service for communicating with FastAPI backend
import { MessageProps } from '../components/MessageComponent';

const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? '/api' 
  : 'http://localhost:8000/api';

const WS_URL = process.env.NODE_ENV === 'production'
  ? `ws://${window.location.host}/ws`
  : 'ws://localhost:8000/ws';

export interface ChatRequest {
  text: string;
  agent_type: 'victim-assistant' | 'operator';
}

export interface ChatResponse {
  id: string;
  text: string;
  sender: string;
  timestamp: string;
  metadata?: {
    tools_executed?: number;
    agent_type?: string;
  };
}

export interface InterAgentMessage {
  id: string;
  timestamp: string;
  type: string;
  sender: string;
  recipient: string;
  content: any;
  priority: string;
}

class ApiService {
  private ws: WebSocket | null = null;
  private wsListeners: ((data: any) => void)[] = [];

  // Initialize WebSocket connection
  initWebSocket() {
    try {
      this.ws = new WebSocket(WS_URL);
      
      this.ws.onopen = () => {
        console.log('🟢 WebSocket connected');
      };
      
      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          this.wsListeners.forEach(listener => listener(data));
        } catch (e) {
          console.log('WebSocket message:', event.data);
        }
      };
      
      this.ws.onclose = () => {
        console.log('🔴 WebSocket disconnected');
        // Attempt to reconnect after 3 seconds
        setTimeout(() => this.initWebSocket(), 3000);
      };
      
      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
    } catch (error) {
      console.error('Failed to initialize WebSocket:', error);
    }
  }

  // Add WebSocket listener
  addWebSocketListener(listener: (data: any) => void) {
    this.wsListeners.push(listener);
  }

  // Remove WebSocket listener
  removeWebSocketListener(listener: (data: any) => void) {
    this.wsListeners = this.wsListeners.filter(l => l !== listener);
  }

  // Send chat message to agent
  async sendChatMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to send message');
    }

    return response.json();
  }

  // Get inter-agent communication log
  async getInterAgentLog(): Promise<{ messages: InterAgentMessage[] }> {
    const response = await fetch(`${API_BASE_URL}/inter-agent-log`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch inter-agent log');
    }
    
    return response.json();
  }

  // Health check
  async healthCheck(): Promise<{
    status: string;
    agents_initialized: boolean;
    communication_system: boolean;
    connected_clients: number;
  }> {
    const response = await fetch(`${API_BASE_URL}/health`);
    
    if (!response.ok) {
      throw new Error('Health check failed');
    }
    
    return response.json();
  }

  // Convert API response to MessageProps format
  convertToMessageProps(response: ChatResponse, userMessage: string): MessageProps[] {
    const messages: MessageProps[] = [];
    
    // Add user message
    messages.push({
      id: Date.now(),
      text: userMessage,
      sender: 'user',
      timestamp: new Date(),
      severity: 'info',
    });
    
    // Add agent response
    messages.push({
      id: Date.now() + 1,
      text: response.text,
      sender: 'assistant',
      timestamp: new Date(response.timestamp),
      severity: 'info',
      metadata: response.metadata,
    });
    
    return messages;
  }
}

export const apiService = new ApiService();

// Initialize WebSocket on module load
apiService.initWebSocket(); 