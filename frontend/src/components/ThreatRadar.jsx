import React, { useState, useEffect } from 'react';
import { 
  ShieldCheck, AlertTriangle, TrendingUp, 
  MapPin, Clock, BarChart3, Zap, Shield, PhoneCall, ExternalLink
} from 'lucide-react';

export default function ThreatRadar({ language = 'hinglish' }) {
  const [stats, setStats] = useState(null);
  const [radarFeed, setRadarFeed] = useState([]);

  useEffect(() => {
    fetchStats();
    fetchRadarFeed();
    const interval = setInterval(() => {
      fetchRadarFeed();
    }, 6000);
    return () => clearInterval(interval);
  }, []);

  const fetchStats = async () => {
    try {
      const res = await fetch('/api/scans/stats');
      const data = await res.json();
      if (data.success) {
        setStats(data.stats);
      }
    } catch (e) {
      console.error("Stats fetch error:", e);
    }
  };

  const fetchRadarFeed = async () => {
    try {
      const res = await fetch('/api/radar/feed');
      const data = await res.json();
      if (data.success) {
        setRadarFeed(data.activeIncidents);
      }
    } catch (e) {
      console.error("Radar feed fetch error:", e);
    }
  };

  return (
    <div className="w-full max-w-6xl mx-auto px-4 sm:px-6 py-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            {language === 'hindi' ? 'राष्ट्रीय साइबर थ्रेट रडार' : 'National Cyber Threat Radar'}
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            {language === 'hindi'
              ? 'भारतीय राज्यों में स्कैम कॉल, फ़िशिंग एसएमएस और डिजिटल अरेस्ट के सक्रिय मामलों की लाइव निगरानी।'
              : 'Real-time telemetry of scam calls, phishing SMS, and extortion attempts across Indian states.'}
          </p>
        </div>

        <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-950/60 border border-emerald-800/40 text-emerald-400 text-xs font-semibold self-start md:self-auto">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          <span>{language === 'hindi' ? 'सुरक्षा सक्रिय है' : 'Live Protection Active'}</span>
        </div>
      </div>

      {/* 4 Stats Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 mb-6">
        <div className="bg-[#111827] border border-slate-800 rounded-xl p-4 sm:p-5">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>{language === 'hindi' ? 'रोके गए खतरे' : 'Threats Blocked'}</span>
            <ShieldCheck className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl sm:text-3xl font-black text-white font-mono">
            {stats ? stats.threatsNeutralized.toLocaleString('en-IN') : '11,894'}
          </div>
          <div className="mt-1 text-xs text-emerald-400 flex items-center gap-1 font-medium">
            <TrendingUp className="w-3 h-3" />
            <span>+14.2% block rate</span>
          </div>
        </div>

        <div className="bg-[#111827] border border-slate-800 rounded-xl p-4 sm:p-5">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>{language === 'hindi' ? 'बचाई गई राशि' : 'Money Saved'}</span>
            <Zap className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl sm:text-3xl font-black text-emerald-400 font-mono">
            ₹{stats ? stats.totalFraudPreventedINR.toLocaleString('en-IN') : '32,45,000'}
          </div>
          <div className="mt-1 text-xs text-slate-400 font-medium">
            <span>{language === 'hindi' ? 'नागरिकों की बचत सुरक्षित' : 'Citizen savings protected'}</span>
          </div>
        </div>

        <div className="bg-[#111827] border border-slate-800 rounded-xl p-4 sm:p-5">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>{language === 'hindi' ? 'सटीकता' : 'Accuracy'}</span>
            <BarChart3 className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl sm:text-3xl font-black text-purple-300 font-mono">
            {stats ? stats.detectionAccuracy : '99.8%'}
          </div>
          <div className="mt-1 text-xs text-slate-400 font-medium">
            <span>{language === 'hindi' ? 'शून्य गलत पहचान' : 'Zero False Positives'}</span>
          </div>
        </div>

        <div className="bg-[#111827] border border-slate-800 rounded-xl p-4 sm:p-5">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium mb-1">
            <span>{language === 'hindi' ? 'एआई गति' : 'AI Speed'}</span>
            <Clock className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl sm:text-3xl font-black text-amber-300 font-mono">
            {stats ? `${stats.responseLatencyMs} ms` : '42 ms'}
          </div>
          <div className="mt-1 text-xs text-slate-400 font-medium">
            <span>{language === 'hindi' ? 'तत्काल विश्लेषण' : 'Instant analysis'}</span>
          </div>
        </div>
      </div>

      {/* Grid: Scam Trends & Live Stream */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Top Scam Types */}
        <div className="lg:col-span-6 bg-[#111827] border border-slate-800 rounded-xl p-5 sm:p-6">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-4">
            {language === 'hindi' ? 'भारत में सबसे आम साइबर अपराध' : 'Most Prevalent Scam Categories in India'}
          </h3>
          <div className="space-y-4">
            {stats?.topScamCategories ? (
              stats.topScamCategories.map((cat, idx) => (
                <div key={idx}>
                  <div className="flex items-center justify-between text-xs mb-1.5">
                    <span className="text-slate-200 font-semibold">{cat.label}</span>
                    <span className="font-mono text-slate-400 text-xs font-medium">
                      {cat.percentage}% ({cat.count.toLocaleString('en-IN')})
                    </span>
                  </div>
                  <div className="w-full h-2 rounded-full bg-slate-900 overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full"
                      style={{ width: `${cat.percentage}%` }}
                    />
                  </div>
                </div>
              ))
            ) : (
              <p className="text-xs text-slate-500">
                {language === 'hindi' ? 'डेटा लोड हो रहा है...' : 'Loading categories...'}
              </p>
            )}
          </div>

          {/* Quick Help Banner */}
          <div className="mt-6 pt-5 border-t border-slate-800 flex items-center justify-between">
            <div>
              <p className="text-xs font-bold text-white">
                {language === 'hindi' ? 'क्या आपके साथ साइबर धोखाधड़ी हुई है?' : 'Faced a cyber fraud?'}
              </p>
              <p className="text-[11px] text-slate-400">
                {language === 'hindi' ? 'तुरंत राष्ट्रीय साइबर हेल्पलाइन पर कॉल करें' : 'Call national helpline immediately'}
              </p>
            </div>
            <a
              href="tel:1930"
              className="px-3.5 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs flex items-center gap-1.5 shadow-sm transition-colors"
            >
              <PhoneCall className="w-3.5 h-3.5" />
              <span>{language === 'hindi' ? '1930 पर कॉल करें' : 'Call 1930'}</span>
            </a>
          </div>
        </div>

        {/* Right: Live Alerts Stream */}
        <div className="lg:col-span-6 bg-[#111827] border border-slate-800 rounded-xl p-5 sm:p-6 flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
              {language === 'hindi' ? 'हाल में रोके गए मामले' : 'Live Intercepted Feed'}
            </h3>
            <span className="text-xs text-cyan-400 font-medium flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse" />
              {language === 'hindi' ? 'स्वचालित अपडेट' : 'Auto-updating'}
            </span>
          </div>

          <div className="space-y-2.5 overflow-y-auto max-h-[380px] pr-1">
            {radarFeed.map((inc) => (
              <div
                key={inc.id}
                className="p-3 rounded-lg bg-slate-900/70 border border-slate-800 hover:border-slate-700 transition-colors flex items-start justify-between gap-3"
              >
                <div>
                  <div className="flex items-center gap-2 text-xs font-bold text-white">
                    <MapPin className="w-3.5 h-3.5 text-cyan-400 flex-shrink-0" />
                    <span>{inc.city}, {inc.state}</span>
                    <span className="text-[10px] px-2 py-0.5 rounded font-mono font-bold bg-rose-950 text-rose-300 border border-rose-800/40">
                      {inc.score}% {language === 'hindi' ? 'खतरा' : 'RISK'}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300 mt-1 font-medium">
                    {inc.category}
                  </p>
                  <span className="text-[11px] text-slate-500 font-mono block mt-0.5">
                    {inc.time}
                  </span>
                </div>

                <div className="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-950/80 text-emerald-300 border border-emerald-800/40 flex-shrink-0">
                  {inc.status}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
