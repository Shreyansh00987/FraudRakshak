/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        obsidian: {
          950: '#060A13',
          900: '#0A0F1D',
          850: '#0E1626',
          800: '#131B2E',
          700: '#1E293B',
          600: '#334155'
        },
        cyber: {
          cyan: '#06B6D4',
          'cyan-bright': '#22D3EE',
          'cyan-glow': 'rgba(6, 182, 212, 0.25)',
          crimson: '#EF4444',
          'crimson-glow': 'rgba(239, 68, 68, 0.25)',
          amber: '#F59E0B',
          emerald: '#10B981',
          'emerald-glow': 'rgba(16, 185, 129, 0.25)',
          violet: '#8B5CF6'
        }
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Fira Code', 'Consolas', 'monospace'],
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'radar-sweep': 'radarSweep 4s linear infinite',
        'glow-pulse': 'glowPulse 2s ease-in-out infinite alternate',
      },
      keyframes: {
        radarSweep: {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },
        glowPulse: {
          '0%': { boxShadow: '0 0 15px rgba(6, 182, 212, 0.3)' },
          '100%': { boxShadow: '0 0 30px rgba(6, 182, 212, 0.7)' },
        }
      }
    },
  },
  plugins: [],
}
