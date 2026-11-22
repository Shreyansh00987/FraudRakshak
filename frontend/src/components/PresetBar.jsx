import React from 'react';
import { HACKATHON_PRESETS } from '../utils/presets';
import { soundSynth } from '../utils/audioSynthesizer';

export default function PresetBar({ onSelectPreset, selectedPresetId, language = 'hinglish' }) {
  const handleSelect = (preset) => {
    onSelectPreset(preset);
  };

  return (
    <div className="w-full bg-[#0D1322] border-b border-slate-800 py-2.5 px-4">
      <div className="max-w-6xl mx-auto flex items-center gap-2 overflow-x-auto scrollbar-none">
        <span className="text-xs font-semibold text-slate-400 flex-shrink-0 mr-1">
          {language === 'hindi' ? 'उदाहरण संदेश:' : 'Test samples:'}
        </span>

        {HACKATHON_PRESETS.map((preset) => {
          const isSelected = selectedPresetId === preset.id;
          const isSafe = preset.tag === 'SAFE';
          const displayName = language === 'hindi' ? preset.nameHindi || preset.name : preset.name;

          return (
            <button
              key={preset.id}
              onClick={() => handleSelect(preset)}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-all flex items-center gap-1.5 flex-shrink-0 cursor-pointer ${
                isSelected
                  ? isSafe
                    ? 'bg-emerald-600 text-white shadow-sm'
                    : 'bg-red-600 text-white shadow-sm'
                  : 'bg-[#1F2937]/60 hover:bg-[#1F2937] text-slate-300 border border-slate-700/60'
              }`}
            >
              <span>{displayName}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
