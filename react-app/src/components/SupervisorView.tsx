import React, { useState } from 'react';
import ChatInterface from './ChatInterface';
import InterAgentLog from './InterAgentLog';
import PanelHeader from './PanelHeader';
import { Ambulance, Heart, Activity, Eye, EyeOff } from 'lucide-react';

const SupervisorView: React.FC = () => {
  const [expandedPanel, setExpandedPanel] = useState<'victim' | 'operator' | 'log' | null>(null);
  const [isMobile, setIsMobile] = useState(window.innerWidth < 1024);

  React.useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 1024);
      if (window.innerWidth >= 1024) {
        setExpandedPanel(null); // Reset expansion on desktop
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const [operatorMessages, setOperatorMessages] = useState([
    {
      id: 1,
      text: "Unit 23 dispatched to 1247 Oak Street. ETA 4 minutes.",
      sender: 'system',
      timestamp: new Date(Date.now() - 3 * 60 * 1000),
      eta: 4,
      severity: 'info',
    },
    {
      id: 2,
      text: "Confirmed. Fire department and paramedics en route. Victim reports active fire on second floor.",
      sender: 'operator',
      timestamp: new Date(Date.now() - 2 * 60 * 1000),
      status: 'warning',
      severity: 'warning',
    },
  ]);

  const [victimMessages, setVictimMessages] = useState([
    {
      id: 1,
      text: "Hello, I'm here to help you. Emergency services have been notified and are on their way. Can you tell me what's happening?",
      sender: 'assistant',
      timestamp: new Date(Date.now() - 4 * 60 * 1000),
      severity: 'info',
      status: 'safe',
    },
    {
      id: 2,
      text: "There's a fire emergency at my location. I need immediate assistance.",
      sender: 'user',
      timestamp: new Date(Date.now() - 3 * 60 * 1000),
    },
    {
      id: 3,
      text: "I understand. Help is on the way. Can you tell me if you're in a safe location right now?",
      sender: 'assistant',
      timestamp: new Date(Date.now() - 2 * 60 * 1000),
      eta: 3,
      severity: 'info',
    },
  ]);

  const [operatorInput, setOperatorInput] = useState('');
  const [victimInput, setVictimInput] = useState('');

  const handleOperatorMessage = (text: string) => {
    if (!text.trim()) return;
    
    const newMessage = {
      id: operatorMessages.length + 1,
      text: text.trim(),
      sender: 'supervisor' as const,
      timestamp: new Date(),
    };
    
    setOperatorMessages(prev => [...prev, newMessage]);
    setOperatorInput('');
  };

  const handleVictimMessage = (text: string) => {
    if (!text.trim()) return;
    
    const newMessage = {
      id: victimMessages.length + 1,
      text: text.trim(),
      sender: 'supervisor' as const,
      timestamp: new Date(),
    };
    
    setVictimMessages(prev => [...prev, newMessage]);
    setVictimInput('');
  };

  const togglePanel = (panel: 'victim' | 'operator' | 'log') => {
    setExpandedPanel(expandedPanel === panel ? null : panel);
  };

  const isVisible = (panel: 'victim' | 'operator' | 'log') => {
    if (!isMobile) return true;
    return expandedPanel === null || expandedPanel === panel;
  };

  const getPanelWidth = (panel: 'victim' | 'operator' | 'log') => {
    if (!isMobile) return 'w-1/3';
    if (expandedPanel === panel) return 'w-full';
    if (expandedPanel === null) return 'w-full';
    return 'w-0 overflow-hidden';
  };

  return (
    <div className="h-screen flex flex-col lg:flex-row">
      {/* Mobile Panel Toggle Bar */}
      {isMobile && (
        <div className="flex bg-base-800 border-b border-base-700 p-2 gap-2">
          <button
            onClick={() => togglePanel('victim')}
            className={`flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-sm font-medium transition-colors ${
              expandedPanel === 'victim' || expandedPanel === null
                ? 'bg-primary-500 text-white'
                : 'bg-base-700 text-base-300'
            }`}
          >
            <Heart size={16} />
            Victim
          </button>
          <button
            onClick={() => togglePanel('log')}
            className={`flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-sm font-medium transition-colors ${
              expandedPanel === 'log' || expandedPanel === null
                ? 'bg-base-700 text-base-100'
                : 'bg-base-600 text-base-400'
            }`}
          >
            <Activity size={16} />
            Log
          </button>
          <button
            onClick={() => togglePanel('operator')}
            className={`flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-sm font-medium transition-colors ${
              expandedPanel === 'operator' || expandedPanel === null
                ? 'bg-base-700 text-base-100'
                : 'bg-base-700 text-base-300'
            }`}
          >
            <Ambulance size={16} />
            911
          </button>
        </div>
      )}

      {/* Left Column - Victim Assistant */}
      <div className={`${getPanelWidth('victim')} border-r border-base-700 flex flex-col transition-all duration-300 ${isVisible('victim') ? '' : 'hidden lg:flex'}`}>
        <PanelHeader
          title="Victim Assistant"
          subtitle="Direct victim support & guidance"
          icon={Heart}
          variant="victim"
          showToggle={isMobile}
          isExpanded={expandedPanel === 'victim'}
          onToggle={() => togglePanel('victim')}
        />
        
        <ChatInterface
          messages={victimMessages}
          inputMessage={victimInput}
          setInputMessage={setVictimInput}
          onSendMessage={handleVictimMessage}
          agentType="victim-assistant"
          compact
        />
      </div>

      {/* Center Column - Inter-Agent Log */}
      <div className={`${getPanelWidth('log')} border-r border-base-700 transition-all duration-300 ${isVisible('log') ? '' : 'hidden lg:block'}`}>
        <InterAgentLog />
      </div>

      {/* Right Column - 911 Operator */}
      <div className={`${getPanelWidth('operator')} flex flex-col transition-all duration-300 ${isVisible('operator') ? '' : 'hidden lg:flex'}`}>
        <PanelHeader
          title="911 Operator"
          subtitle="Emergency dispatch coordination"
          icon={Ambulance}
          variant="operator"
          showToggle={isMobile}
          isExpanded={expandedPanel === 'operator'}
          onToggle={() => togglePanel('operator')}
        />
        
        <ChatInterface
          messages={operatorMessages}
          inputMessage={operatorInput}
          setInputMessage={setOperatorInput}
          onSendMessage={handleOperatorMessage}
          agentType="operator"
          compact
        />
      </div>
    </div>
  );
};

export default SupervisorView;