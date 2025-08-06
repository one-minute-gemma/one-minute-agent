import React from 'react';
import { Flame, Heart, Car, AlertTriangle } from 'lucide-react';

interface QuickActionsProps {
  onAction: (action: string) => void;
}

const QuickActions: React.FC<QuickActionsProps> = ({ onAction }) => {
  const actions = [
    {
      id: 'fire',
      label: 'Fire',
      icon: Flame,
      color: 'bg-red-600 hover:bg-red-700 border border-red-500 hover:border-red-400',
      severity: 'danger',
    },
    {
      id: 'medical',
      label: 'Medical',
      icon: Heart,
      color: 'bg-green-600 hover:bg-green-700 border border-green-500 hover:border-green-400',
      severity: 'warning',
    },
    {
      id: 'accident',
      label: 'Accident',
      icon: Car,
      color: 'bg-orange-600 hover:bg-orange-700 border border-orange-500 hover:border-orange-400',
      severity: 'warning',
    },
  ];

  return (
    <div className="mt-4">
      <p className="text-sm text-base-400 mb-3 text-center">Quick emergency categories:</p>
      <div className="grid grid-cols-3 gap-3">
        {actions.map((action) => (
          <button
            key={action.id}
            onClick={() => onAction(action.id)}
            className={`${action.color} text-base-50 rounded-lg p-4 flex flex-col items-center gap-2 transition-all duration-200 touch-manipulation hover:scale-105 active:scale-95 shadow-lg hover:shadow-xl group`}
          >
            <action.icon size={24} className="text-white" />
            <span className="font-medium text-sm">{action.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default QuickActions;