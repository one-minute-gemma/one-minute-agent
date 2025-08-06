import React from 'react';
import { Clock, AlertTriangle, CheckCircle2, Activity, Wifi } from 'lucide-react';

interface LogEntry {
  id: string;
  timestamp: string;
  type: 'system' | 'dispatch' | 'status' | 'coordination';
  severity: 'info' | 'warning' | 'critical';
  message: string;
  eta?: number;
}

const InterAgentLog: React.FC = () => {
  const logEntries: LogEntry[] = [
    {
      id: '1',
      timestamp: '18:42:15',
      type: 'system',
      severity: 'info',
      message: 'Emergency call received - Medical emergency reported'
    },
    {
      id: '2',
      timestamp: '18:42:18',
      type: 'dispatch',
      severity: 'info',
      message: 'Unit 23 dispatched to 1234 Main St',
      eta: 4
    },
    {
      id: '3',
      timestamp: '18:42:45',
      type: 'coordination',
      severity: 'warning',
      message: 'Victim reports difficulty breathing - priority elevated'
    },
    {
      id: '4',
      timestamp: '18:43:12',
      type: 'status',
      severity: 'info',
      message: 'Unit 23 en route - ETA updated',
      eta: 3
    },
    {
      id: '5',
      timestamp: '18:43:28',
      type: 'coordination',
      severity: 'critical',
      message: 'Victim Assistant: Instructed victim to unlock door and sit down'
    }
  ];

  const getStatusIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
        return <AlertTriangle className="w-3 h-3 text-status-danger" />;
      case 'warning':
        return <AlertTriangle className="w-3 h-3 text-status-warning" />;
      default:
        return <CheckCircle2 className="w-3 h-3 text-status-safe" />;
    }
  };

  const getSeverityBorder = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'border-l-status-danger';
      case 'warning':
        return 'border-l-status-warning';
      default:
        return 'border-l-primary-500';
    }
  };

  return (
    <div className="h-full flex flex-col bg-base-900">
      {/* Header */}
      <div className="p-4 border-b border-base-700 bg-base-800/80 backdrop-blur-sm">
        <div className="flex items-center justify-between min-h-[64px]">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-base-700/50 text-base-300">
              <Activity size={20} />
            </div>
            <div>
              <h2 className="font-semibold text-lg text-base-50">Inter-Agent Communication</h2>
              <p className="text-sm text-base-400 mt-0.5">Real-time coordination log</p>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-status-safe rounded-full animate-pulse"></div>
              <span className="text-xs text-base-300">911 Operator Online</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-status-safe rounded-full animate-pulse"></div>
              <span className="text-xs text-base-300">Victim Assistant Online</span>
            </div>
          </div>
        </div>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {logEntries.map((entry) => (
          <div
            key={entry.id}
            className={`p-3 bg-base-800 rounded border-l-2 ${getSeverityBorder(entry.severity)} font-mono text-sm`}
          >
            <div className="flex items-center justify-between mb-1">
              <div className="flex items-center gap-2">
                {getStatusIcon(entry.severity)}
                <span className="text-base-300 text-xs">{entry.timestamp}</span>
                <span className={`text-xs uppercase tracking-wide font-semibold ${
                  entry.type === 'dispatch' ? 'text-primary-400' :
                  entry.type === 'coordination' ? 'text-status-warning' :
                  entry.type === 'system' ? 'text-status-info' :
                  'text-base-400'
                }`}>
                  {entry.type}
                </span>
              </div>
              {entry.eta && (
                <span className="text-primary-400 text-xs font-semibold">
                  ETA: {entry.eta}min
                </span>
              )}
            </div>
            <div className="text-base-100 leading-relaxed">
              {entry.message}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default InterAgentLog;