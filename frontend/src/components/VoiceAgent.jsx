import React, { useState } from 'react';
import { 
  Mic, MicOff, Volume2, Send, 
  MessageSquare, User, Bot
} from 'lucide-react';
import AudioWaveform from './AudioWaveform';
import { speechEngine } from '../utils/speechEngine';
import { soundSynth } from '../utils/audioSynthesizer';

const QUICK_PROMPTS = [
  { 
    icon: "⚡", 
    label: "Bijli Cutoff SMS", 
    labelHindi: "बिजली बिल कटऑफ",
    query: "Bhaiya mujhe bijli cut ka message aaya hai, kya karu?",
    queryHindi: "भैया मुझे बिजली कट का मैसेज आया है, क्या करूँ?"
  },
  { 
    icon: "🏦", 
    label: "Bank OTP Demand", 
    labelHindi: "बैंक ओटीपी मांगना",
    query: "Bank manager bol raha hai turant OTP batao varna account block hoga",
    queryHindi: "बैंक मैनेजर बोल रहा है तुरंत ओटीपी बताओ वरना खाता बंद होगा"
  },
  { 
    icon: "👮", 
    label: "Digital Arrest Call", 
    labelHindi: "डिजिटल अरेस्ट कॉल",
    query: "CBI officer bol raha hai narcotics parcel me mera naam aaya hai",
    queryHindi: "सीबीआई ऑफिसर बोल रहा है नारकोटिक्स पार्सल में मेरा नाम आया है"
  },
  { 
    icon: "🎟️", 
    label: "KBC 25 Lakh Lottery", 
    labelHindi: "केबीसी 25 लाख लॉटरी",
    query: "WhatsApp par call aaya hai ki KBC 25 lakh lottery jeeti hai",
    queryHindi: "व्हाट्सएप पर कॉल आया है कि केबीसी 25 लाख लॉटरी जीती है"
  },
  { 
    icon: "💳", 
    label: "PhonePe QR Cashback", 
    labelHindi: "फोनपे क्यूआर कैशबैक",
    query: "PhonePe par Rs 4,999 lene ke liye QR scan karne ko bola hai",
    queryHindi: "फोनपे पर 4999 रुपये लेने के लिए क्यूआर स्कैन करने को बोला है"
  }
];

export default function VoiceAgent({ language = 'hinglish' }) {
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [transcriptInput, setTranscriptInput] = useState('');
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      sender: 'bot',
      textHindi: "नमस्ते! मैं आपका रक्षक एआई वॉइस एडवाइज़र हूँ। यदि आपको कोई संदिग्ध कॉल या संदेश आया है, तो माइक दबाकर बोलिए या लिखकर पूछिए।",
      textHinglish: "Namaste! Main aapka Rakshak AI voice advisor hoon. Agar aapko koi sandigdh call ya message aaya hai, toh mic dabakar boliye ya likhkar poochiye.",
      textEnglish: "Hello! I am your Rakshak AI voice advisor. If you received any suspicious call or message, tap the mic and speak, or type your question.",
      timestamp: "Just now",
      riskLevel: "SAFE"
    }
  ]);

  const handleToggleMic = () => {
    if (isListening) {
      speechEngine.stopListening();
      setIsListening(false);
    } else {
      speechEngine.stopSpeaking();
      setIsSpeaking(false);
      setIsListening(true);

      speechEngine.startListening({
        onResult: ({ final, interim }) => {
          if (final) {
            setTranscriptInput(final);
            handleSendQuery(final);
            speechEngine.stopListening();
            setIsListening(false);
          } else {
            setTranscriptInput(interim);
          }
        },
        onError: () => setIsListening(false),
        onEnd: () => setIsListening(false)
      }, language === 'english' ? 'en-IN' : 'hi-IN');
    }
  };

  const handleSendQuery = async (queryText) => {
    const text = queryText || transcriptInput;
    if (!text || !text.trim()) return;

    const userMsg = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    setTranscriptInput('');

    try {
      const res = await fetch('/api/voice/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: text })
      });
      const data = await res.json();
      const answer = data.data;

      const botMsg = {
        id: `bot-${Date.now()}`,
        sender: 'bot',
        textHindi: answer.response_text_hindi,
        textHinglish: answer.response_text_hinglish,
        textEnglish: answer.response_text_english,
        spokenScript: answer.spoken_audio_script,
        riskLevel: answer.risk_level,
        category: answer.detected_category,
        actions: answer.bullet_actions,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages((prev) => [...prev, botMsg]);
      speakBotMessage(botMsg);
    } catch (e) {
      console.error("Voice query failed:", e);
    }
  };

  const speakBotMessage = (botMsg) => {
    let textToSpeak = botMsg.textHinglish;
    if (language === 'english') {
      textToSpeak = botMsg.textEnglish;
    } else if (language === 'hindi') {
      textToSpeak = botMsg.textHindi || botMsg.spokenScript || botMsg.textHinglish;
    } else {
      textToSpeak = botMsg.spokenScript || botMsg.textHinglish;
    }

    const langCode = language === 'english' ? 'en-IN' : 'hi-IN';

    setIsSpeaking(true);
    speechEngine.speak(textToSpeak, {
      lang: langCode,
      rate: 0.95,
      onEnd: () => setIsSpeaking(false),
      onError: () => setIsSpeaking(false)
    });
  };

  const getBotDisplayText = (m) => {
    if (language === 'hindi') {
      return m.textHindi || m.textHinglish;
    }
    if (language === 'english') {
      return m.textEnglish;
    }
    return m.textHinglish;
  };

  return (
    <div className="w-full max-w-4xl mx-auto px-4 sm:px-6 py-6">
      {/* Title */}
      <div className="text-center mb-6">
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          {language === 'hindi' ? 'रक्षक वॉइस एआई एडवाइज़र' : 'Rakshak Voice AI'}
        </h1>
        <p className="text-sm text-slate-400 mt-1">
          {language === 'hindi'
            ? 'माइक दबाकर हिंदी में बोलें — हमारा एआई तुरंत स्कैम का विश्लेषण कर आपको सुरक्षित करेगा।'
            : language === 'english'
            ? 'Speak in English or Hindi — our AI will analyze the scam and guide you safely.'
            : 'Speak in Hindi or English — our AI will analyze the scam and guide you safely.'}
        </p>
      </div>

      {/* Voice Assistant Center Card */}
      <div className="bg-[#111827] border border-slate-800 rounded-2xl p-6 sm:p-8 flex flex-col items-center shadow-lg mb-6">
        {/* Equalizer waveform */}
        <div className="w-full max-w-xs mb-4">
          <AudioWaveform
            isActive={isListening || isSpeaking}
            color={isListening ? 'crimson' : isSpeaking ? 'cyan' : 'emerald'}
          />
        </div>

        {/* Big Mic Button */}
        <div className="relative my-2">
          <button
            onClick={handleToggleMic}
            className={`w-20 h-20 sm:w-24 sm:h-24 rounded-full flex items-center justify-center transition-all duration-200 cursor-pointer shadow-lg ${
              isListening
                ? 'bg-rose-600 text-white shadow-rose-600/50 scale-105'
                : isSpeaking
                ? 'bg-cyan-500 text-slate-950 shadow-cyan-500/50'
                : 'bg-cyan-500 hover:bg-cyan-400 text-slate-950 shadow-cyan-500/30 hover:scale-105'
            }`}
          >
            {isListening ? (
              <MicOff className="w-9 h-9 sm:w-10 sm:h-10" />
            ) : isSpeaking ? (
              <Volume2 className="w-9 h-9 sm:w-10 sm:h-10 animate-pulse" />
            ) : (
              <Mic className="w-9 h-9 sm:w-10 sm:h-10" />
            )}
          </button>
        </div>

        {/* State label */}
        <div className="text-center mt-3">
          <p className="text-sm font-semibold text-white">
            {isListening ? (
              <span className="text-rose-400">
                {language === 'hindi' ? 'आपकी बात सुन रहे हैं... बोलिए' : 'Listening to you... speak now'}
              </span>
            ) : isSpeaking ? (
              <span className="text-cyan-400">
                {language === 'hindi' ? 'रक्षक एआई बोल रहा है...' : 'Rakshak AI speaking out loud...'}
              </span>
            ) : (
              language === 'hindi' ? 'माइक पर क्लिक करें और बोलें' : 'Tap the microphone to speak'
            )}
          </p>
          <p className="text-xs text-slate-400 mt-0.5">
            {language === 'hindi' ? 'हिंदी, हिंग्लिश और अंग्रेज़ी में उपलब्ध' : 'Works in Hindi, Hinglish, and English'}
          </p>
        </div>

        {/* Quick Example Scenarios */}
        <div className="w-full mt-6 pt-5 border-t border-slate-800">
          <p className="text-xs font-semibold text-slate-400 mb-2.5 text-center">
            {language === 'hindi' ? 'या इन उदाहरणों में से कोई एक चुनें:' : 'Or tap an example question:'}
          </p>
          <div className="flex flex-wrap items-center justify-center gap-2">
            {QUICK_PROMPTS.map((prompt, idx) => {
              const label = language === 'hindi' ? prompt.labelHindi : prompt.label;
              const query = language === 'hindi' ? prompt.queryHindi : prompt.query;
              return (
                <button
                  key={idx}
                  onClick={() => {
                    setTranscriptInput(query);
                    handleSendQuery(query);
                  }}
                  className="px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700 border border-slate-700 text-xs text-slate-200 hover:text-white transition-colors cursor-pointer flex items-center gap-1.5"
                >
                  <span>{prompt.icon}</span>
                  <span>{label}</span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Conversation Thread */}
      <div className="bg-[#111827] border border-slate-800 rounded-2xl p-4 sm:p-6 shadow-lg">
        <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4 flex items-center gap-2">
          <MessageSquare className="w-4 h-4 text-cyan-400" />
          <span>{language === 'hindi' ? 'बातचीत का विवरण' : 'Conversation'}</span>
        </h3>

        <div className="space-y-3 max-h-[380px] overflow-y-auto pr-1">
          {messages.map((m) => {
            const isBot = m.sender === 'bot';
            return (
              <div
                key={m.id}
                className={`flex gap-3 ${isBot ? 'items-start' : 'items-start flex-row-reverse'}`}
              >
                {/* Avatar */}
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 text-xs font-bold ${
                    isBot
                      ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30'
                      : 'bg-slate-700 text-slate-200'
                  }`}
                >
                  {isBot ? <Bot className="w-4 h-4" /> : <User className="w-4 h-4" />}
                </div>

                {/* Bubble */}
                <div
                  className={`max-w-[85%] rounded-2xl p-4 text-sm leading-relaxed ${
                    isBot
                      ? 'bg-[#1e293b] border border-slate-700/60 text-slate-100'
                      : 'bg-cyan-600 text-white font-medium'
                  }`}
                >
                  <p>{isBot ? getBotDisplayText(m) : m.text}</p>

                  {/* Bullet actions if present */}
                  {m.actions && m.actions.length > 0 && (
                    <div className="mt-3 pt-3 border-t border-slate-700/60 text-xs">
                      <p className="font-semibold text-cyan-400 mb-1.5">
                        {language === 'hindi' ? 'आपको क्या करना चाहिए:' : 'What you should do:'}
                      </p>
                      <ul className="space-y-1 text-slate-300">
                        {m.actions.map((act, i) => (
                          <li key={i} className="flex items-start gap-1.5">
                            <span className="text-cyan-400 font-bold">•</span>
                            <span>{act}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Replay audio */}
                  {isBot && m.id !== 'welcome' && (
                    <div className="mt-3 pt-2 border-t border-slate-700/60 flex items-center justify-between">
                      <button
                        onClick={() => speakBotMessage(m)}
                        className="inline-flex items-center gap-1.5 text-xs font-semibold text-cyan-400 hover:text-cyan-300 transition-colors cursor-pointer"
                      >
                        <Volume2 className="w-3.5 h-3.5" />
                        <span>{language === 'hindi' ? 'आवाज़ दोबारा सुनें' : 'Listen Again (आवाज़ सुनें)'}</span>
                      </button>
                      <span className="text-[11px] text-slate-400">{m.timestamp}</span>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* Text Input Footer */}
        <div className="mt-4 pt-3 border-t border-slate-800 flex items-center gap-2">
          <input
            type="text"
            placeholder={
              language === 'hindi'
                ? 'यहाँ अपना प्रश्न हिंदी में लिखें...'
                : 'Type your question in Hindi or English...'
            }
            value={transcriptInput}
            onChange={(e) => setTranscriptInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSendQuery()}
            className="flex-1 px-4 py-2.5 text-sm bg-slate-900 border border-slate-700 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
          />
          <button
            onClick={() => handleSendQuery()}
            disabled={!transcriptInput.trim()}
            className="px-4 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold rounded-xl text-sm transition-colors cursor-pointer disabled:opacity-50 flex items-center gap-1.5"
          >
            <Send className="w-4 h-4" />
            <span className="hidden sm:inline">{language === 'hindi' ? 'भेजें' : 'Send'}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
