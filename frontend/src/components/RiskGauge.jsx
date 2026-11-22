import React from 'react';
import { ShieldAlert, ShieldCheck, AlertTriangle } from 'lucide-react';

export default function RiskGauge({ score = 0, severity = 'SAFE', size = 150 }) {
  const strokeWidth = 10;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (circumference * Math.min(100, Math.max(0, score))) / 100;

  // Colors based on score
  let strokeColor = '#10B981'; // Green (Safe)
  let textColor = 'text-emerald-400';
  let badgeClass = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
  let severityLabel = 'SAFE / LEGITIMATE';
  let Icon = ShieldCheck;

  if (score >= 80 || severity === 'CRITICAL') {
    strokeColor = '#EF4444'; // Red (Danger)
    textColor = 'text-red-400';
    badgeClass = 'bg-red-500/10 text-red-400 border-red-500/20';
    severityLabel = 'HIGH RISK SCAM';
    Icon = ShieldAlert;
  } else if (score >= 40 || severity === 'HIGH' || severity === 'SUSPICIOUS') {
    strokeColor = '#F59E0B'; // Amber
    textColor = 'text-amber-400';
    badgeClass = 'bg-amber-500/10 text-amber-400 border-amber-500/20';
    severityLabel = 'SUSPICIOUS';
    Icon = AlertTriangle;
  }

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="relative" style={{ width: size, height: size }}>
        <svg
          width={size}
          height={size}
          viewBox={`0 0 ${size} ${size}`}
          className="transform -rotate-90"
        >
          {/* Background Track */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke="#1F2937"
            strokeWidth={strokeWidth}
          />
          {/* Animated Indicator */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke={strokeColor}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            style={{
              transition: 'stroke-dashoffset 0.8s ease-out, stroke 0.3s ease'
            }}
          />
        </svg>

        {/* Center Readout */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className={`text-3xl font-extrabold ${textColor}`}>
            {score}%
          </span>
          <span className="text-[10px] font-medium text-slate-400 uppercase tracking-wider">
            Risk
          </span>
        </div>
      </div>

      {/* Status Pill */}
      <div className={`mt-2 inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-bold border ${badgeClass}`}>
        <Icon className="w-3.5 h-3.5" />
        <span>{severityLabel}</span>
      </div>
    </div>
  );
}
