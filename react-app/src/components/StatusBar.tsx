import React, { useState, useEffect } from 'react';
import { Clock, CheckCircle2, Shield } from 'lucide-react';

const StatusBar: React.FC = () => {
  const [eta, setEta] = useState(5);
  const [pulseActive, setPulseActive] = useState(true);

  useEffect(() => {
    const interval = setInterval(() => {
      setEta(prev => {
        const newEta = Math.max(0, prev - 1);
        if (newEta === 0) setPulseActive(false);
        return newEta;
      });
    }, 60000); // Update every minute

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-gradient-to-r from-base-800 to-base-700 text-base-50 px-6 py-4 shadow-lg border-b border-primary-500/20">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={`p-3 rounded-full bg-primary-500/20 border border-primary-500/30 ${pulseActive ? 'animate-glow' : ''}`}>
              {eta > 0 ? (
                <Shield size={24} className="text-primary-400" />
              ) : (
                <CheckCircle2 size={24} className="text-status-safe" />
              )}
            </div>
            <div>
              <h1 className="text-lg font-semibold">
                {eta > 0 ? 'Help is on the way' : 'Emergency responders have arrived'}
              </h1>
              <p className="text-base-300 text-sm">
                {eta > 0 ? 'Emergency services have been notified' : 'You are now in safe hands'}
              </p>
            </div>
          </div>
          
          <div className={`flex items-center gap-2 px-4 py-2 rounded-lg ${
            eta > 0 
              ? 'bg-base-800/50 backdrop-blur-sm border border-primary-500/30' 
              : 'bg-status-safe/20 border border-status-safe/50 animate-pulse'
          }`}>
            <Clock size={20} className={eta > 0 ? 'text-primary-400' : 'text-status-safe'} />
            <span className="font-bold text-lg">
              ETA: {eta > 0 ? `${eta} min` : 'Arriving now'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StatusBar;