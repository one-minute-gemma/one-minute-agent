import React from 'react';
import { DivideIcon as LucideIcon } from 'lucide-react';

interface PanelHeaderProps {
  title: string;
  subtitle: string;
  icon: LucideIcon;
  variant: 'victim' | 'operator' | 'system';
  onToggle?: () => void;
  isExpanded?: boolean;
  showToggle?: boolean;
}

const PanelHeader: React.FC<PanelHeaderProps> = ({
  title,
  subtitle,
  icon: Icon,
  variant,
  onToggle,
  isExpanded,
  showToggle = false,
}) => {
  const getVariantStyles = (variant: string) => {
    switch (variant) {
      case 'victim':
        return {
          bg: 'bg-base-800/80',
          border: 'border-primary-500/30',
          text: 'text-base-50',
          icon: 'text-primary-400',
          subtitle: 'text-base-300',
        };
      case 'operator':
        return {
          bg: 'bg-base-800/80',
          border: 'border-base-600/30',
          text: 'text-base-50',
          icon: 'text-base-300',
          subtitle: 'text-base-400',
        };
      case 'system':
      default:
        return {
          bg: 'bg-base-800/80',
          border: 'border-base-600/30',
          text: 'text-base-50',
          icon: 'text-base-300',
          subtitle: 'text-base-400',
        };
    }
  };

  const styles = getVariantStyles(variant);

  return (
    <div className={`p-4 border-b ${styles.border} ${styles.bg} backdrop-blur-sm`}>
      <div className="flex items-center justify-between min-h-[64px]">
        <div className="flex items-center gap-3">
          <div className={`p-2 rounded-lg bg-base-700/50 ${styles.icon}`}>
            <Icon size={20} />
          </div>
          <div>
            <h2 className={`font-semibold text-lg ${styles.text}`}>{title}</h2>
            <p className={`text-sm ${styles.subtitle} mt-0.5`}>{subtitle}</p>
          </div>
        </div>
        
        {showToggle && onToggle && (
          <button
            onClick={onToggle}
            className={`px-3 py-1 rounded-md text-sm font-medium transition-all duration-200 ${
              isExpanded 
                ? `bg-primary-500 text-white` 
                : `bg-base-700 text-base-300 hover:bg-primary-500 hover:text-white`
            }`}
          >
            {isExpanded ? 'Collapse' : 'Expand'}
          </button>
        )}
      </div>
    </div>
  );
};

export default PanelHeader;