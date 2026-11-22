import React, { useState } from 'react';
import Navbar from './components/Navbar';
import PresetBar from './components/PresetBar';
import ThreatAnalyzer from './components/ThreatAnalyzer';
import VoiceAgent from './components/VoiceAgent';
import ScamCallSimulator from './components/ScamCallSimulator';
import Complaint1930Modal from './components/Complaint1930Modal';
import { HACKATHON_PRESETS } from './utils/presets';
import { Shield, PhoneCall, ExternalLink } from 'lucide-react';

export default function App() {
  const [language, setLanguage] = useState('hinglish');
  const [activeTab, setActiveTab] = useState('analyzer');
  const [isMuted, setIsMuted] = useState(false);
  const [selectedPresetId, setSelectedPresetId] = useState(null);

  // Shared state for Analyzer input
  const [analyzerText, setAnalyzerText] = useState(HACKATHON_PRESETS[1].text);
  const [senderNumber, setSenderNumber] = useState(HACKATHON_PRESETS[1].sender);

  // 1930 Complaint Modal State
  const [is1930ModalOpen, setIs1930ModalOpen] = useState(false);
  const [modalInitialData, setModalInitialData] = useState(null);

  const handleSelectPreset = (preset) => {
    setSelectedPresetId(preset.id);
    setAnalyzerText(preset.text);
    setSenderNumber(preset.sender || '');
    setActiveTab('analyzer');
  };

  const handleOpen1930Modal = (data) => {
    setModalInitialData(data);
    setIs1930ModalOpen(true);
  };

  return (
    <div className="min-h-screen bg-[#0B0F19] text-slate-100 flex flex-col font-sans selection:bg-cyan-500 selection:text-slate-950">
      {/* Clean Navbar */}
      <Navbar
        language={language}
        setLanguage={setLanguage}
        isMuted={isMuted}
        setIsMuted={setIsMuted}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
      />

      {/* Preset Scenarios Strip */}
      <PresetBar
        onSelectPreset={handleSelectPreset}
        selectedPresetId={selectedPresetId}
        language={language}
      />

      {/* Main Tabbed Content Area */}
      <main className="flex-1 pb-20 md:pb-12">
        {activeTab === 'analyzer' && (
          <ThreatAnalyzer
            inputText={analyzerText}
            setInputText={setAnalyzerText}
            senderNumber={senderNumber}
            setSenderNumber={setSenderNumber}
            onOpen1930Modal={handleOpen1930Modal}
            selectedPresetId={selectedPresetId}
            language={language}
          />
        )}

        {activeTab === 'voice' && (
          <VoiceAgent
            language={language}
          />
        )}

        {activeTab === 'simulator' && (
          <ScamCallSimulator
            onOpen1930Modal={handleOpen1930Modal}
            language={language}
          />
        )}
      </main>

      {/* 1930 Cyber Crime Complaint Modal */}
      <Complaint1930Modal
        isOpen={is1930ModalOpen}
        onClose={() => setIs1930ModalOpen(false)}
        initialData={modalInitialData}
      />

      {/* Clean Footer */}
      <footer className="border-t border-slate-800/80 bg-[#070b14] py-4 text-xs text-slate-400 mb-16 md:mb-0">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 flex flex-col sm:flex-row items-center justify-between gap-3 text-center sm:text-left">
          <div className="flex items-center gap-2">
            <Shield className="w-4 h-4 text-cyan-400 flex-shrink-0" />
            <span className="font-bold text-white">fraudRakshak</span>
            <span className="text-slate-500 hidden sm:inline">— AI Scam Shield for India</span>
          </div>

          <div className="flex items-center gap-4 text-xs">
            <a
              href="tel:1930"
              className="flex items-center gap-1.5 text-rose-400 hover:text-rose-300 font-semibold"
            >
              <PhoneCall className="w-3.5 h-3.5" />
              <span>National Cyber Helpline 1930</span>
            </a>
            <span className="text-slate-700">|</span>
            <a
              href="https://cybercrime.gov.in"
              target="_blank"
              rel="noreferrer"
              className="text-cyan-400 hover:text-cyan-300 flex items-center gap-1 font-semibold"
            >
              <span>cybercrime.gov.in</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
