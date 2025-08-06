import React, { useState, useEffect } from 'react';
import VictimView from './components/VictimView';
import SupervisorView from './components/SupervisorView';
import { Monitor, Smartphone } from 'lucide-react';

function App() {
  const [currentView, setCurrentView] = useState<'victim' | 'supervisor'>('victim');
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkScreenSize = () => {
      setIsMobile(window.innerWidth < 1024);
      // Auto-switch to victim view on mobile, supervisor on desktop
      if (window.innerWidth < 1024) {
        setCurrentView('victim');
      } else {
        setCurrentView('supervisor');
      }
    };

    checkScreenSize();
    window.addEventListener('resize', checkScreenSize);
    return () => window.removeEventListener('resize', checkScreenSize);
  }, []);

  const toggleView = () => {
    setCurrentView(currentView === 'victim' ? 'supervisor' : 'victim');
  };

  return (
    <div className="min-h-screen bg-base-900 text-base-50 font-inter">
      {/* View Toggle - Only show on desktop */}
      {!isMobile && (
        <button
          onClick={toggleView}
          className="fixed top-4 right-4 z-50 flex items-center gap-2 px-4 py-2 bg-primary-500 hover:bg-primary-600 rounded-lg transition-all duration-200 text-sm font-medium text-white shadow-lg hover:shadow-xl"
        >
          {currentView === 'victim' ? (
            <>
              <Monitor size={16} />
              Supervisor View
            </>
          ) : (
            <>
              <Smartphone size={16} />
              Victim View
            </>
          )}
        </button>
      )}

      {currentView === 'victim' ? <VictimView /> : <SupervisorView />}
    </div>
  );
}

export default App;