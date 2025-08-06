import React, { useEffect, useRef } from 'react';
import { Send } from 'lucide-react';
import MessageComponent, { MessageProps } from './MessageComponent';

interface ChatInterfaceProps {
  messages: MessageProps[];
  inputMessage: string;
  setInputMessage: (message: string) => void;
  onSendMessage: (message: string) => void;
  agentType: 'victim-assistant' | 'operator';
  compact?: boolean;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({
  messages,
  inputMessage,
  setInputMessage,
  onSendMessage,
  agentType,
  compact = false,
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSendMessage(inputMessage);
  };

  return (
    <div className="flex flex-col h-full min-h-0">
      {/* Messages */}
      <div className={`flex-1 overflow-y-auto p-4 ${compact ? 'text-sm' : ''} bg-gradient-to-b from-base-950/50 to-base-900/80 min-h-0`}>
        {messages.map((message) => (
          <MessageComponent
            key={message.id}
            message={message}
            compact={compact}
            agentType={agentType}
          />
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-base-700 p-4 bg-base-800/50 backdrop-blur-sm">
        <form onSubmit={handleSubmit} className="flex gap-3">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Type your message..."
            className={`flex-1 bg-base-800 border border-base-600 rounded-lg px-4 py-3 text-base-100 placeholder-base-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 ${compact ? 'py-2 text-sm' : ''}`}
          />
          <button
            type="submit"
            disabled={!inputMessage.trim()}
            className={`bg-primary-500 hover:bg-primary-600 disabled:bg-base-700 disabled:cursor-not-allowed rounded-lg px-4 py-3 text-white transition-all duration-200 hover:scale-105 active:scale-95 shadow-lg hover:shadow-xl ${compact ? 'py-2' : ''}`}
          >
            <Send size={compact ? 16 : 20} />
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatInterface;