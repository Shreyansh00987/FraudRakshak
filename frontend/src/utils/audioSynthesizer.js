/**
 * Web Audio API Sound Synthesizer
 * Generates synthetic telephone ringtones, high-priority alert sirens,
 * radar pings, and UI chimes. 100% browser-native with zero dependencies.
 */

class SoundSynthesizer {
  constructor() {
    this.ctx = null;
    this.activeRingtone = null;
    this.activeSiren = null;
    this.isMuted = false;
  }

  init() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) {
        this.ctx = new AudioCtx();
      }
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  setMuted(muted) {
    this.isMuted = muted;
    if (muted) {
      this.stopRingtone();
      this.stopSiren();
    }
  }

  // Realistic Indian PSTN Telephone Ringtone (Call Simulator)
  playRingtone() {
    if (this.isMuted) return;
    this.init();
    if (!this.ctx) return;
    this.stopRingtone();

    let isRinging = true;

    const ringBurst = () => {
      if (!isRinging || !this.ctx) return;

      const now = this.ctx.currentTime;
      const osc1 = this.ctx.createOscillator();
      const osc2 = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc1.type = 'sine';
      osc2.type = 'sine';
      osc1.frequency.setValueAtTime(400, now);
      osc2.frequency.setValueAtTime(450, now);

      // Pulse 1: 0.4s
      gain.gain.setValueAtTime(0, now);
      gain.gain.linearRampToValueAtTime(0.25, now + 0.05);
      gain.gain.setValueAtTime(0.25, now + 0.4);
      gain.gain.linearRampToValueAtTime(0, now + 0.45);

      // Pulse 2: 0.4s (after 0.2s pause)
      gain.gain.setValueAtTime(0, now + 0.65);
      gain.gain.linearRampToValueAtTime(0.25, now + 0.7);
      gain.gain.setValueAtTime(0.25, now + 1.1);
      gain.gain.linearRampToValueAtTime(0, now + 1.15);

      osc1.connect(gain);
      osc2.connect(gain);
      gain.connect(this.ctx.destination);

      osc1.start(now);
      osc2.start(now);
      osc1.stop(now + 1.2);
      osc2.stop(now + 1.2);
    };

    ringBurst();
    const interval = setInterval(ringBurst, 3200);

    this.activeRingtone = {
      stop: () => {
        isRinging = false;
        clearInterval(interval);
      }
    };
  }

  stopRingtone() {
    if (this.activeRingtone) {
      this.activeRingtone.stop();
      this.activeRingtone = null;
    }
  }

  // Original High-Priority Cyber Threat Warning Siren (Oscillating 650Hz - 1100Hz)
  playSiren() {
    if (this.isMuted) return;
    this.init();
    if (!this.ctx) return;
    this.stopSiren();

    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    const now = this.ctx.currentTime;

    osc.type = 'sawtooth';
    gain.gain.setValueAtTime(0.15, now);

    // Modulate pitch between 650Hz and 1100Hz
    for (let i = 0; i < 5; i++) {
      const t = now + i * 0.35;
      osc.frequency.setValueAtTime(650, t);
      osc.frequency.linearRampToValueAtTime(1100, t + 0.18);
      osc.frequency.linearRampToValueAtTime(650, t + 0.35);
    }

    gain.gain.setValueAtTime(0.15, now + 1.7);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 2.0);

    osc.connect(gain);
    gain.connect(this.ctx.destination);

    osc.start(now);
    osc.stop(now + 2.1);

    this.activeSiren = osc;
  }

  stopSiren() {
    if (this.activeSiren) {
      try {
        this.activeSiren.stop();
      } catch (e) {}
      this.activeSiren = null;
    }
  }

  // Radar Ping Sonar Effect
  playRadarPing() {
    if (this.isMuted) return;
    this.init();
    if (!this.ctx) return;

    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    const now = this.ctx.currentTime;

    osc.type = 'sine';
    osc.frequency.setValueAtTime(1250, now);
    osc.frequency.exponentialRampToValueAtTime(450, now + 0.3);

    gain.gain.setValueAtTime(0.2, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);

    osc.connect(gain);
    gain.connect(this.ctx.destination);

    osc.start(now);
    osc.stop(now + 0.36);
  }

  // Safe Transaction Chime (Harmonic C major arpeggio)
  playSuccessChime() {
    if (this.isMuted) return;
    this.init();
    if (!this.ctx) return;

    const notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
    const now = this.ctx.currentTime;

    notes.forEach((freq, idx) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      const t = now + idx * 0.08;

      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, t);

      gain.gain.setValueAtTime(0.15, t);
      gain.gain.exponentialRampToValueAtTime(0.001, t + 0.35);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(t);
      osc.stop(t + 0.4);
    });
  }

  playClick() {
    // Kept quiet during standard UI navigation
  }
}

export const soundSynth = new SoundSynthesizer();
