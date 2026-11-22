import React, { useState, useEffect, useRef } from 'react';
import { 
  ShieldAlert, ShieldCheck, AlertTriangle, Mic, MicOff, 
  Volume2, VolumeX, FileText, RefreshCw, Send, Link2, PhoneCall
} from 'lucide-react';
import confetti from 'canvas-confetti';
import RiskGauge from './RiskGauge';
import { soundSynth } from '../utils/audioSynthesizer';
import { speechEngine } from '../utils/speechEngine';

export default function ThreatAnalyzer({ 
  inputText, 
  setInputText, 
  senderNumber, 
  setSenderNumber, 
  onOpen1930Modal,
  selectedPresetId = null,
  language = 'hinglish' 
}) {
  const [isScanning, setIsScanning] = useState(false);
  const [isDictating, setIsDictating] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isSpeakingWarning, setIsSpeakingWarning] = useState(false);

  // Auto-scan on preset change: ALWAYS silent (Zero sound on mount or preset switch)
  useEffect(() => {
    if (inputText && inputText.trim()) {
      handleAnalyze(inputText, false); // Always silent when clicking presets or loading
    }
  }, [selectedPresetId]);

  // Toggle Voice Dictation (STT)
  const toggleDictation = () => {
    if (isDictating) {
      speechEngine.stopListening();
      setIsDictating(false);
    } else {
      setIsDictating(true);
      speechEngine.startListening({
        onResult: ({ final, interim }) => {
          if (final) {
            setInputText((prev) => (prev ? `${prev} ${final}` : final));
          }
        },
        onError: () => setIsDictating(false),
        onEnd: () => setIsDictating(false)
      }, language === 'english' ? 'en-IN' : 'hi-IN');
    }
  };

  // Perform Threat Scan (Sound plays ONLY when user explicitly clicks "Check for Scam" button)
  const handleAnalyze = async (overrideText = null, isUserClick = false) => {
    const textToAnalyze = overrideText || inputText;
    if (!textToAnalyze || !textToAnalyze.trim()) return;

    setIsScanning(true);

    try {
      const response = await fetch('/api/scans/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: textToAnalyze,
          sender: senderNumber || 'Unknown'
        })
      });

      const res = await response.json();
      const data = res.data;
      setAnalysisResult(data);

      // Sound plays ONLY AND EXCLUSIVELY when user clicks the "Check for Scam" button
      if (isUserClick) {
        if (data.riskScore >= 60) {
          soundSynth.playSiren();
        } else if (data.riskScore <= 20) {
          soundSynth.playSuccessChime();
          confetti({
            particleCount: 50,
            spread: 60,
            origin: { y: 0.7 }
          });
        }
      }
    } catch (err) {
      console.error("Scan failed:", err);
    } finally {
      setIsScanning(false);
    }
  };

  // Play Spoken Voice Warning (TTS)
  const handlePlayVoiceWarning = () => {
    if (isSpeakingWarning) {
      speechEngine.stopSpeaking();
      setIsSpeakingWarning(false);
      return;
    }

    if (!analysisResult || !analysisResult.voiceWarningScript) return;

    const script = language === 'english' 
      ? analysisResult.voiceWarningScript.en 
      : analysisResult.voiceWarningScript.hi;

    const langCode = language === 'english' ? 'en-IN' : 'hi-IN';

    setIsSpeakingWarning(true);
    speechEngine.speak(script, {
      lang: langCode,
      rate: 0.95,
      onEnd: () => setIsSpeakingWarning(false),
      onError: () => setIsSpeakingWarning(false)
    });
  };

  // Get active explanation text based on language
  const getExplanation = () => {
    if (!analysisResult?.explanations) return '';
    if (language === 'hindi') {
      return analysisResult.explanations.hindi || analysisResult.explanations.hinglish;
    }
    if (language === 'english') {
      return analysisResult.explanations.english;
    }
    return analysisResult.explanations.hinglish;
  };

  // Render markdown bold, backticks and bullets cleanly
  const renderFormattedExplanation = (text) => {
    if (!text) return null;
    return text.split('\n').map((line, lIdx) => {
      const trimmed = line.trim();
      if (!trimmed) {
        return <div key={lIdx} className="h-2" />;
      }

      const isBullet = trimmed.startsWith('•');
      const content = isBullet ? trimmed.substring(1).trim() : trimmed;
      const segments = content.split(/(\*\*.*?\*\*|`.*?`)/g);

      return (
        <div key={lIdx} className={`${isBullet ? 'flex items-start gap-2 ml-1 my-1.5' : 'my-1'} text-sm leading-relaxed text-slate-200`}>
          {isBullet && <span className="text-amber-400 font-bold flex-shrink-0 mt-0.5">•</span>}
          <span>
            {segments.map((seg, sIdx) => {
              if (seg.startsWith('**') && seg.endsWith('**')) {
                return <strong key={sIdx} className="text-white font-semibold">{seg.slice(2, -2)}</strong>;
              }
              if (seg.startsWith('`') && seg.endsWith('`')) {
                return (
                  <code key={sIdx} className="px-1.5 py-0.5 mx-0.5 rounded bg-slate-800 border border-slate-700 text-amber-300 font-mono text-xs">
                    {seg.slice(1, -1)}
                  </code>
                );
              }
              return seg;
            })}
          </span>
        </div>
      );
    });
  };

  return (
    <div className="w-full max-w-4xl mx-auto px-4 sm:px-6 py-6">
      {/* Page Header */}
      <div className="text-center mb-6">
        <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
          {language === 'hindi' 
            ? 'क्या यह संदेश कोई स्कैम या फ्रॉड है?' 
            : language === 'english'
            ? 'Is that message a scam?'
            : 'Kya yeh message scam hai? (Check Now)'}
        </h1>
        <p className="text-sm text-slate-400 mt-1 max-w-lg mx-auto">
          {language === 'hindi'
            ? 'किसी भी संदिग्ध एसएमएस, व्हाट्सएप या कॉल नंबर को नीचे पेस्ट करें और यूपीआई फ्रॉड, बैंक केवाईसी, बिजली बिल व डिजिटल अरेस्ट की जांच करें।'
            : language === 'english'
            ? 'Paste any SMS, WhatsApp forward, or number below. We check for UPI traps, fake bank KYC, power cutoff panic, and digital arrest threats.'
            : 'Paste any SMS, WhatsApp forward, or number below. Hum UPI trap, fake bank KYC, bijli cut panic aur digital arrest threats check karte hain.'}
        </p>
      </div>

      {/* Main Input Box */}
      <div className="bg-[#111827] border border-slate-800 rounded-2xl p-4 sm:p-5 shadow-xl mb-6">
        <div className="flex items-center justify-between mb-2">
          <label className="text-xs font-semibold text-slate-400">
            {language === 'hindi' ? 'संदेश या फ़ोन नंबर दर्ज करें:' : 'Message or Phone Number:'}
          </label>
          <div className="flex items-center gap-2">
            <button
              onClick={toggleDictation}
              className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-medium transition-colors cursor-pointer ${
                isDictating
                  ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                  : 'bg-slate-800 text-slate-300 hover:text-white'
              }`}
            >
              {isDictating ? <MicOff className="w-3.5 h-3.5 text-red-400" /> : <Mic className="w-3.5 h-3.5 text-blue-400" />}
              <span>
                {isDictating 
                  ? (language === 'hindi' ? 'सुन रहे हैं...' : 'Listening...') 
                  : (language === 'hindi' ? 'बोलकर लिखें' : 'Voice Dictate')}
              </span>
            </button>

            {inputText && (
              <button
                onClick={() => { setInputText(''); setAnalysisResult(null); }}
                className="text-xs text-slate-500 hover:text-slate-300 cursor-pointer"
              >
                {language === 'hindi' ? 'साफ़ करें' : 'Clear'}
              </button>
            )}
          </div>
        </div>

        {/* Text Input */}
        <textarea
          rows={4}
          placeholder={
            language === 'hindi'
              ? 'यहाँ एसएमएस पेस्ट करें... जैसे: आपका खाता ब्लॉक हो जाएगा, तुरंत केवाईसी करें...'
              : 'Paste SMS here... e.g. Aapka khata block ho jayega, turant KYC karo...'
          }
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          className="w-full p-3 text-sm bg-[#0B0F19] border border-slate-800 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-blue-500 resize-none font-sans leading-relaxed"
        />

        {/* Sender field (optional) */}
        <div className="mt-3 flex flex-col sm:flex-row items-center gap-3">
          <input
            type="text"
            placeholder={
              language === 'hindi'
                ? 'भेजने वाले का नंबर या हेडर (वैकल्पिक, जैसे +92..., VM-SBINB)'
                : 'Sender number/header (optional, e.g. +92..., VM-SBINB)'
            }
            value={senderNumber}
            onChange={(e) => setSenderNumber(e.target.value)}
            className="w-full sm:w-2/3 px-3 py-2 text-xs bg-[#0B0F19] border border-slate-800 rounded-xl text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500"
          />

          <button
            onClick={() => handleAnalyze(null, true)}
            disabled={isScanning || !inputText.trim()}
            className="w-full sm:w-1/3 py-2.5 px-4 rounded-xl font-bold text-xs bg-blue-600 hover:bg-blue-500 text-white transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
          >
            {isScanning ? (
              <>
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                <span>{language === 'hindi' ? 'जाँच हो रही है...' : 'Checking...'}</span>
              </>
            ) : (
              <span>{language === 'hindi' ? 'स्कैम की जाँच करें' : 'Check for Scam'}</span>
            )}
          </button>
        </div>
      </div>

      {/* Analysis Result */}
      {analysisResult && (
        <div className={`p-5 rounded-2xl border transition-all ${
          analysisResult.riskScore >= 60
            ? 'bg-[#181116] border-red-500/40 text-slate-100'
            : 'bg-[#0E1715] border-emerald-500/40 text-slate-100'
        }`}>
          {/* Verdict Header */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-4">
            <div className="flex items-center gap-3">
              {analysisResult.riskScore >= 60 ? (
                <div className="p-3 rounded-xl bg-red-500/20 text-red-400 flex-shrink-0">
                  <ShieldAlert className="w-7 h-7" />
                </div>
              ) : (
                <div className="p-3 rounded-xl bg-emerald-500/20 text-emerald-400 flex-shrink-0">
                  <ShieldCheck className="w-7 h-7" />
                </div>
              )}
              <div>
                <span className="text-xs uppercase font-bold tracking-wider text-slate-400">
                  {analysisResult.riskScore >= 60 
                    ? (language === 'hindi' ? '🚨 खतरनाक फ्रॉड / स्कैम डिटेक्ट हुआ' : '🚨 Dangerous Threat Detected')
                    : (language === 'hindi' ? '✅ सुरक्षित बैंक सूचना' : '✅ Verified Safe Notification')}
                </span>
                <h2 className="text-xl font-extrabold text-white">
                  {analysisResult.categoryName} ({analysisResult.riskScore}% {language === 'hindi' ? 'जोखिम' : 'Risk'})
                </h2>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center gap-2">
              <button
                onClick={handlePlayVoiceWarning}
                className="px-3.5 py-2 rounded-xl text-xs font-bold bg-[#111827] hover:bg-slate-800 border border-slate-700 text-slate-200 transition-colors flex items-center gap-1.5 cursor-pointer"
              >
                {isSpeakingWarning ? <VolumeX className="w-4 h-4 text-red-400" /> : <Volume2 className="w-4 h-4 text-blue-400" />}
                <span>
                  {isSpeakingWarning 
                    ? (language === 'hindi' ? 'आवाज़ रोकें' : 'Stop Voice') 
                    : (language === 'hindi' ? '🔊 आवाज़ में सुनें' : '🔊 Listen in Audio')}
                </span>
              </button>

              {analysisResult.riskScore >= 60 && (
                <button
                  onClick={() => onOpen1930Modal(analysisResult)}
                  className="px-3.5 py-2 rounded-xl text-xs font-bold bg-red-600 hover:bg-red-500 text-white transition-colors flex items-center gap-1.5 cursor-pointer"
                >
                  <FileText className="w-4 h-4" />
                  <span>{language === 'hindi' ? '1930 पर रिपोर्ट करें' : 'Report 1930'}</span>
                </button>
              )}
            </div>
          </div>

          {/* Explanation in Selected Language */}
          <div className="py-4">
            <h3 className="text-xs font-bold uppercase text-slate-400 mb-2">
              {language === 'hindi' ? 'संदेश का वास्तविक विश्लेषण व सुरक्षा सलाह:' : 'Message Analysis & Safety Advice:'}
            </h3>
            <div className="bg-[#111827]/80 rounded-xl p-3.5 border border-slate-800 font-sans">
              {renderFormattedExplanation(getExplanation())}
            </div>
          </div>

          {/* Red flags list (if any) */}
          {analysisResult.redFlags && analysisResult.redFlags.length > 0 && (
            <div className="pt-3 border-t border-slate-800/80">
              <h4 className="text-xs font-bold uppercase text-red-400 mb-2">
                {language === 'hindi' ? 'यह संदेश क्यों खतरनाक है:' : 'Why this is dangerous:'}
              </h4>
              <ul className="space-y-1.5 text-xs text-slate-300">
                {analysisResult.redFlags.map((flag, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="text-red-400 font-bold">•</span>
                    <span>
                      <strong className="text-white">{flag.title}:</strong> {flag.description}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Action Recommendations */}
          <div className="mt-4 pt-3 border-t border-slate-800/80 flex flex-wrap items-center gap-2 text-xs">
            <span className="font-bold text-slate-400">
              {language === 'hindi' ? 'आपको क्या करना चाहिए:' : 'What you should do:'}
            </span>
            {analysisResult.actionRecommendations?.slice(0, 3).map((act, i) => (
              <span key={i} className="px-2.5 py-1 rounded-md bg-[#111827] border border-slate-800 text-slate-300">
                {act}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
