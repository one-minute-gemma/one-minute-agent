import React from 'react';
import { CheckCircle2, AlertTriangle, Info, Clock, Shield, Heart, Bot } from 'lucide-react';

export interface MessageProps {
  id: number;
  text: string;
  sender: 'user' | 'assistant' | 'operator' | 'supervisor' | 'system';
  timestamp: Date;
  severity?: 'info' | 'warning' | 'danger' | 'success';
  eta?: number;
  status?: 'safe' | 'warning' | 'danger';
}

interface MessageComponentProps {
  message: MessageProps;
  compact?: boolean;
  agentType?: 'victim-assistant' | 'operator' | 'system';
}

const MessageComponent: React.FC<MessageComponentProps> = ({ 
  message, 
  compact = false, 
  agentType = 'victim-assistant' 
}) => {
  const getSenderConfig = (sender: string, agentType: string) => {
    switch (sender) {
      case 'user':
        return {
          label: 'You',
          bgColor: 'bg-primary-500',
          textColor: 'text-white',
          alignment: 'ml-auto',
          icon: null,
          containerAlignment: 'flex justify-end',
        };
      case 'assistant':
        return {
          label: agentType === 'victim-assistant' ? 'Assistant' : 'Victim Assistant',
          bgColor: 'bg-base-700',
          textColor: 'text-base-50',
          alignment: 'mr-auto',
          icon: Bot,
          containerAlignment: 'flex justify-start',
        };
      case 'operator':
        return {
          label: '911 Operator',
          bgColor: 'bg-base-700 border border-base-600',
          textColor: 'text-base-50',
          alignment: 'ml-auto',
          icon: Shield,
          containerAlignment: 'flex justify-end',
        };
      case 'supervisor':
        return {
          label: 'Supervisor',
          bgColor: 'bg-base-700 border border-base-600',
          textColor: 'text-base-50',
          alignment: 'ml-auto',
          icon: CheckCircle2,
          containerAlignment: 'flex justify-end',
        };
      case 'system':
        return {
          label: 'System',
          bgColor: 'bg-base-800 border border-base-700',
          textColor: 'text-base-200',
          alignment: 'mr-auto',
          icon: Bot,
          containerAlignment: 'flex justify-start',
        };
      default:
        return {
          label: sender,
          bgColor: 'bg-base-800 border border-base-700',
          textColor: 'text-base-200',
          alignment: 'mr-auto',
          icon: null,
          containerAlignment: 'flex justify-start',
        };
    }
  };

  const getSeverityBorder = (severity?: string) => {
    switch (severity) {
      case 'success':
        return 'border-l-4 border-l-status-safe';
      case 'warning':
        return 'border-l-4 border-l-status-warning';
      case 'danger':
        return 'border-l-4 border-l-status-danger';
      case 'info':
      default:
        return '';
    }
  };

  const getSeverityIcon = (severity?: string) => {
    switch (severity) {
      case 'success':
        return <CheckCircle2 size={12} className="text-status-safe" />;
      case 'warning':
        return <AlertTriangle size={12} className="text-status-warning" />;
      case 'danger':
        return <AlertTriangle size={12} className="text-status-danger" />;
      case 'info':
      default:
        return null;
    }
  };

  const getStatusIndicator = (status?: string) => {
    switch (status) {
      case 'safe':
        return <CheckCircle2 size={12} className="text-status-safe" />;
      case 'warning':
        return <AlertTriangle size={12} className="text-status-warning" />;
      case 'danger':
        return <AlertTriangle size={12} className="text-status-danger" />;
      default:
        return null;
    }
  };

  const config = getSenderConfig(message.sender, agentType);
  const Icon = config.icon;
  const severityBorder = getSeverityBorder(message.severity);

  return (
    <div className={`${config.containerAlignment} animate-fade-in mb-3`}>
      <div className={`max-w-xs sm:max-w-md lg:max-w-lg px-4 py-3 rounded-lg ${config.bgColor} ${config.textColor} ${compact ? 'max-w-xs' : ''} shadow-lg ${severityBorder}`}>
        {/* Header */}
        <div className="flex items-center gap-2 mb-2">
          {Icon && (
            <div className="flex items-center gap-1">
              <Icon size={12} className="opacity-75" />
              {(message.sender === 'assistant' || message.sender === 'system') && (
                <div className="w-2 h-2 bg-status-safe rounded-full animate-pulse"></div>
              )}
            </div>
          )}
          <span className="text-xs font-medium opacity-90">
            {config.label}
          </span>
          <span className="text-xs opacity-60 font-mono">
            {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
          {message.severity && getSeverityIcon(message.severity)}
          {message.status && getStatusIndicator(message.status)}
        </div>

        {/* Message Content */}
        <p className={`${compact ? 'text-sm' : ''} leading-relaxed`}>
          {message.text}
        </p>

        {/* ETA Display */}
        {message.eta && (
          <div className="flex items-center gap-2 mt-2 pt-2 border-t border-white/10">
            <Clock size={12} className="text-primary-300" />
            <span className="text-sm font-medium">
              ETA: {message.eta > 0 ? `${message.eta} min` : 'Arriving now'}
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageComponent;