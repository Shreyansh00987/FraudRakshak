/**
 * Speech Engine: Multilingual STT & TTS
 * Integrates Web Speech Recognition & Speech Synthesis for Hindi and Indian English.
 */

class SpeechEngine {
  constructor() {
    this.recognition = null;
    this.synthesis = window.speechSynthesis;
    this.currentUtterance = null;
    this.isListening = false;
    this.isSpeaking = false;
    this.voices = [];
    this.preferredLang = 'hi-IN'; // Default Hindi / Hinglish

    if (typeof window !== 'undefined') {
      this.initVoices();
      if ('speechSynthesis' in window) {
        window.speechSynthesis.onvoiceschanged = () => this.initVoices();
      }
    }
  }

  initVoices() {
    if (!this.synthesis) return;
    this.voices = this.synthesis.getVoices();
  }

  getBestVoice(lang = 'hi-IN') {
    if (!this.voices || this.voices.length === 0) {
      this.initVoices();
    }
    
    // Look for exact lang match
    let match = this.voices.find(v => v.lang === lang || v.lang.replace('_', '-') === lang);
    if (match) return match;

    // Look for lang family (e.g. 'hi')
    const langFamily = lang.split('-')[0];
    match = this.voices.find(v => v.lang.startsWith(langFamily));
    if (match) return match;

    // Look for Indian English as second best natural choice for Hinglish
    match = this.voices.find(v => v.lang === 'en-IN' || v.lang.includes('India'));
    if (match) return match;

    // Fallback to any English or default
    return this.voices.find(v => v.lang.startsWith('en')) || this.voices[0] || null;
  }

  speak(text, options = {}) {
    if (!this.synthesis) {
      console.warn("Speech synthesis not supported in this browser.");
      if (options.onEnd) options.onEnd();
      return;
    }

    this.stopSpeaking();

    const utterance = new SpeechSynthesisUtterance(text);
    const lang = options.lang || this.preferredLang;
    utterance.lang = lang;
    
    const voice = this.getBestVoice(lang);
    if (voice) {
      utterance.voice = voice;
    }

    utterance.rate = options.rate || 0.95; // Slightly measured pace for authoritative clarity
    utterance.pitch = options.pitch || 1.0;

    utterance.onstart = () => {
      this.isSpeaking = true;
      if (options.onStart) options.onStart();
    };

    utterance.onend = () => {
      this.isSpeaking = false;
      this.currentUtterance = null;
      if (options.onEnd) options.onEnd();
    };

    utterance.onerror = (e) => {
      console.error("TTS Speech synthesis error:", e);
      this.isSpeaking = false;
      this.currentUtterance = null;
      if (options.onError) options.onError(e);
      if (options.onEnd) options.onEnd();
    };

    this.currentUtterance = utterance;
    this.synthesis.speak(utterance);
  }

  stopSpeaking() {
    if (this.synthesis) {
      this.synthesis.cancel();
      this.isSpeaking = false;
      this.currentUtterance = null;
    }
  }

  startListening(callbacks = {}, lang = 'hi-IN') {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      console.warn("Speech Recognition not supported in this browser environment.");
      if (callbacks.onError) callbacks.onError("NOT_SUPPORTED");
      return;
    }

    this.stopListening();

    try {
      this.recognition = new SpeechRecognition();
      this.recognition.lang = lang;
      this.recognition.continuous = callbacks.continuous !== false;
      this.recognition.interimResults = true;

      this.recognition.onstart = () => {
        this.isListening = true;
        if (callbacks.onStart) callbacks.onStart();
      };

      this.recognition.onresult = (event) => {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; ++i) {
          const item = event.results[i];
          if (item.isFinal) {
            finalTranscript += item[0].transcript;
          } else {
            interimTranscript += item[0].transcript;
          }
        }

        if (callbacks.onResult) {
          callbacks.onResult({ final: finalTranscript, interim: interimTranscript });
        }
      };

      this.recognition.onerror = (e) => {
        console.warn("Speech recognition error:", e.error);
        if (callbacks.onError) callbacks.onError(e.error);
      };

      this.recognition.onend = () => {
        this.isListening = false;
        if (callbacks.onEnd) callbacks.onEnd();
      };

      this.recognition.start();
    } catch (err) {
      console.error("Failed to start speech recognition:", err);
      if (callbacks.onError) callbacks.onError(err.message);
    }
  }

  stopListening() {
    if (this.recognition) {
      try {
        this.recognition.stop();
      } catch (e) {}
      this.isListening = false;
      this.recognition = null;
    }
  }
}

export const speechEngine = new SpeechEngine();
