// Hook for inter-agent communication log
import { useState, useEffect, useCallback } from 'react';
import { apiService, InterAgentMessage } from '../services/api';

interface UseInterAgentLogReturn {
  messages: InterAgentMessage[];
  isLoading: boolean;
  error: string | null;
  refresh: () => Promise<void>;
}

export const useInterAgentLog = (): UseInterAgentLogReturn => {
  const [messages, setMessages] = useState<InterAgentMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchMessages = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await apiService.getInterAgentLog();
      setMessages(response.messages);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch messages');
      console.error('Inter-agent log error:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Real-time updates via WebSocket
  useEffect(() => {
    const handleWebSocketMessage = (data: any) => {
      if (data.type === 'agent_response' || data.type === 'inter_agent_message') {
        // Refresh log when new messages arrive
        fetchMessages();
      }
    };

    apiService.addWebSocketListener(handleWebSocketMessage);
    
    return () => {
      apiService.removeWebSocketListener(handleWebSocketMessage);
    };
  }, [fetchMessages]);

  // Initial fetch and periodic updates
  useEffect(() => {
    fetchMessages();
    
    // Refresh every 5 seconds
    const interval = setInterval(fetchMessages, 5000);
    
    return () => clearInterval(interval);
  }, [fetchMessages]);

  return {
    messages,
    isLoading,
    error,
    refresh: fetchMessages,
  };
}; 