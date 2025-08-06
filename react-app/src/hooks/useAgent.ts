// Custom hook for agent communication
import { useState, useCallback, useEffect } from 'react';
import { apiService, ChatRequest } from '../services/api';
import { MessageProps } from '../components/MessageComponent';

interface UseAgentReturn {
  messages: MessageProps[];
  isLoading: boolean;
  error: string | null;
  sendMessage: (text: string) => Promise<void>;
  clearMessages: () => void;
}

export const useAgent = (agentType: 'victim-assistant' | 'operator'): UseAgentReturn => {
  const [messages, setMessages] = useState<MessageProps[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Initialize with welcome message
  useEffect(() => {
    const welcomeMessage: MessageProps = {
      id: 1,
      text: agentType === 'victim-assistant' 
        ? "Hello, I'm here to help you. Emergency services have been notified and are on their way. Can you tell me what's happening?"
        : "911 Emergency Services. Units are being dispatched. Please provide situation update.",
      sender: 'assistant',
      timestamp: new Date(),
      severity: 'info',
      status: 'safe',
    };
    
    setMessages([welcomeMessage]);
  }, [agentType]);

  const sendMessage = useCallback(async (text: string) => {
    if (!text.trim()) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      // Add user message immediately
      const userMessage: MessageProps = {
        id: Date.now(),
        text: text.trim(),
        sender: 'user',
        timestamp: new Date(),
        severity: 'info',
      };
      
      setMessages(prev => [...prev, userMessage]);
      
      // Send to agent
      const request: ChatRequest = {
        text: text.trim(),
        agent_type: agentType,
      };
      
      const response = await apiService.sendChatMessage(request);
      
      // Add agent response
      const agentMessage: MessageProps = {
        id: Date.now() + 1,
        text: response.text,
        sender: 'assistant',
        timestamp: new Date(response.timestamp),
        severity: 'info',
        metadata: response.metadata,
      };
      
      setMessages(prev => [...prev, agentMessage]);
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message');
      console.error('Agent communication error:', err);
    } finally {
      setIsLoading(false);
    }
  }, [agentType]);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    clearMessages,
  };
}; 