import React from 'react';
import { Shield, Volume2, VolumeX, Globe, Scan, Mic, PhoneCall, FileText } from 'lucide-react';
import { soundSynth } from '../utils/audioSynthesizer';

export default function Navbar({ language, setLanguage, isMuted, setIsMuted, activeTab, setActiveTab }) {
  const toggleMute = () => {
    const nextState = !isMuted;
    setIsMuted(nextState);
    soundSynth.setMuted(nextState);
  };

  const navTabs = [
    { 
      id: 'analyzer', 
      label: language === 'hindi' ? 'संदेश जांचें' : 'Scan Message', 
      icon: <Scan className="w-4 h-4" /> 
    },
    { 
      id: 'voice', 
      label: language === 'hindi' ? 'वॉइस एआई' : 'Voice AI', 
      icon: <Mic className="w-4 h-4" /> 
    },
    { 
      id: 'simulator', 
      label: language === 'hindi' ? 'कॉल डेमो' : 'Call Demo', 
      icon: <PhoneCall className="w-4 h-4" /> 
    }
  ];

  const handleLangChange = (lang) => {
    setLanguage(lang);
  };

  return (
    <header className="sticky top-0 z-40 bg-[#0B0F19]/95 border-b border-slate-800 backdrop-blur-md">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div 
            className="flex items-center gap-2.5 cursor-pointer" 
            onClick={() => setActiveTab('analyzer')}
          >
            <div className="w-9 h-9 rounded-xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center text-blue-400">
              <Shield className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-lg font-bold text-white tracking-tight">
                  fraud<span className="text-blue-400">Rakshak</span>
                </span>
                <span className="w-2 h-2 rounded-full bg-emerald-400" title="Shield Active" />
              </div>
              <p className="text-[11px] text-slate-400 hidden sm:block">
                {language === 'hindi' ? 'एआई फ्रॉड कॉल व एसएमएस सुरक्षा' : 'AI Scam Call & SMS Shield'}
              </p>
            </div>
          </div>

          {/* Clean Segmented Tab Control (Desktop) */}
          <nav className="hidden md:flex items-center bg-[#111827] p-1 rounded-xl border border-slate-800">
            {navTabs.map((tab) => {
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`px-3.5 py-1.5 text-xs font-semibold rounded-lg transition-all flex items-center gap-1.5 cursor-pointer ${
                    isActive
                      ? 'bg-blue-600 text-white shadow-sm'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  <span>{tab.icon}</span>
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Controls: Language Buttons + Sound */}
          <div className="flex items-center gap-2">
            {/* Prominent Clickable Language Segmented Buttons */}
            <div className="flex items-center bg-[#111827] border border-slate-800 rounded-lg p-1 text-xs">
              <button
                onClick={() => handleLangChange('hinglish')}
                className={`px-2.5 py-1 rounded-md font-semibold transition-all cursor-pointer ${
                  language === 'hinglish'
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                Hinglish
              </button>
              <button
                onClick={() => handleLangChange('hindi')}
                className={`px-2.5 py-1 rounded-md font-semibold transition-all cursor-pointer ${
                  language === 'hindi'
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                हिंदी
              </button>
              <button
                onClick={() => handleLangChange('english')}
                className={`px-2.5 py-1 rounded-md font-semibold transition-all cursor-pointer ${
                  language === 'english'
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                English
              </button>
            </div>

            <button
              onClick={toggleMute}
              title={isMuted ? "Unmute Sound" : "Mute Sound"}
              className={`p-2 rounded-lg border transition-colors cursor-pointer ${
                isMuted
                  ? 'bg-red-500/10 border-red-500/30 text-red-400'
                  : 'bg-[#111827] border-slate-800 text-slate-400 hover:text-white'
              }`}
            >
              {isMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
            </button>
          </div>
        </div>
      </div>

      {/* Clean Mobile Bottom Nav Bar */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 z-50 bg-[#111827] border-t border-slate-800 px-2 py-1.5 flex items-center justify-around shadow-2xl">
        {navTabs.map((tab) => {
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex-1 py-1.5 flex flex-col items-center justify-center gap-1 transition-colors ${
                isActive ? 'text-blue-400 font-bold' : 'text-slate-400'
              }`}
            >
              <span>{tab.icon}</span>
              <span className="text-[10px]">{tab.label}</span>
            </button>
          );
        })}
      </div>
    </header>
  );
}
