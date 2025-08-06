import React, { useState } from 'react';
import StatusBar from './StatusBar';
import ChatInterface from './ChatInterface';
import QuickActions from './QuickActions';
import { useAgent } from '../hooks/useAgent';

const VictimView: React.FC = () => {
  const { messages, isLoading, error, sendMessage } = useAgent('victim-assistant');
  const [inputMessage, setInputMessage] = useState('');
  const [quickActionsUsed, setQuickActionsUsed] = useState(false);

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;
    await sendMessage(text);
    setInputMessage('');
  };

  const handleQuickAction = async (action: string) => {
    const actionMessages = {
      fire: "There's a fire emergency at my location. I need immediate assistance.",
      medical: "I need medical assistance. Someone is injured and needs help.",
      accident: "There's been an accident. We need emergency response immediately.",
    };

    const message = actionMessages[action as keyof typeof actionMessages];
    if (message) {
      await handleSendMessage(message);
      setQuickActionsUsed(true);
    }
  };

  return (
    <div className="h-screen flex flex-col">
      <StatusBar />
      
      <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full px-4 pb-4 min-h-0">
        {error && (
          <div className="bg-status-danger/20 border border-status-danger/30 rounded-lg p-3 mb-4 text-status-danger text-sm">
            ⚠️ {error}
          </div>
        )}
        
        <ChatInterface
          messages={messages}
          inputMessage={inputMessage}
          setInputMessage={setInputMessage}
          onSendMessage={handleSendMessage}
          agentType="victim-assistant"
          isLoading={isLoading}
        />
        
        {!quickActionsUsed && <QuickActions onAction={handleQuickAction} />}
      </div>
    </div>
  );
};

export default VictimView;