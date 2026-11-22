import React, { useState, useEffect } from 'react';
import { 
  X, FileText, Copy, Check, Download, ExternalLink, Shield
} from 'lucide-react';
import { soundSynth } from '../utils/audioSynthesizer';

export default function Complaint1930Modal({ isOpen, onClose, initialData = null }) {
  const [victimName, setVictimName] = useState('Rahul Verma');
  const [victimPhone, setVictimPhone] = useState('+91 98100 23456');
  const [victimState, setVictimState] = useState('Delhi NCR');
  const [financialLoss, setFinancialLoss] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [filedReport, setFiledReport] = useState(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setFiledReport(null);
      if (initialData?.preventedAmount) {
        setFinancialLoss(initialData.preventedAmount);
      }
    }
  }, [isOpen, initialData]);

  if (!isOpen) return null;

  const suspectPhone = initialData?.sender || initialData?.suspectNumber || initialData?.iocs?.phoneNumbers?.[0] || '+92 301 9876543';
  const suspectUrls = initialData?.iocs?.urls?.map(u => u.url || u.domain).join(', ') || 'Direct Telephonic Deception';
  const incidentCategory = initialData?.categoryName || initialData?.scamCategory || 'UPI & NetBanking Phishing Extortion';
  const evidenceSummary = initialData?.text || 'Scam communication with extortion and psychological urgency.';

  const handleGenerateAndSubmit = async () => {
    setIsSubmitting(true);
    soundSynth.playRadarPing();

    try {
      const res = await fetch('/api/reports/1930', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          victimName,
          victimPhone,
          victimState,
          victimCity: victimState,
          incidentCategory,
          suspectNumbers: suspectPhone,
          suspectUrls: suspectUrls,
          financialLossINR: financialLoss,
          evidenceSummary: evidenceSummary,
          bankName: "Nationalized Bank / Public Authority"
        })
      });

      const data = await res.json();
      if (data.success) {
        setFiledReport(data.data);
        soundSynth.playSuccessChime();
      }
    } catch (e) {
      console.error("Complaint filing failed:", e);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleCopyText = (text) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadTxt = () => {
    if (!filedReport) return;
    const blob = new Blob([filedReport.complaintText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Cyber-Crime-Complaint-${filedReport.complaintId}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm overflow-y-auto">
      <div className="relative w-full max-w-2xl rounded-2xl bg-[#111827] border border-slate-700 shadow-2xl overflow-hidden my-6">
        {/* Header */}
        <div className="flex items-center justify-between p-5 sm:p-6 border-b border-slate-800 bg-[#0b0f19]">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-rose-500/20 text-rose-400 border border-rose-500/30 flex items-center justify-center">
              <Shield className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base sm:text-lg font-bold text-white">
                1930 National Cyber Crime Complaint
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">
                Generates a formal legal police complaint draft (cybercrime.gov.in)
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition-colors cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-5 sm:p-6 space-y-4 max-h-[75vh] overflow-y-auto">
          {!filedReport ? (
            <>
              {/* Incident Summary Pill */}
              <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 text-xs space-y-1.5">
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Scam Type:</span>
                  <span className="text-rose-400 font-semibold">{incidentCategory}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Suspect Phone:</span>
                  <span className="text-amber-300 font-mono font-medium">{suspectPhone}</span>
                </div>
                {suspectUrls && suspectUrls !== 'Direct Telephonic Deception' && (
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400">Phishing Link:</span>
                    <span className="text-cyan-400 font-mono truncate max-w-[280px]">{suspectUrls}</span>
                  </div>
                )}
              </div>

              {/* Form Inputs */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1">
                    Your Name
                  </label>
                  <input
                    type="text"
                    value={victimName}
                    onChange={(e) => setVictimName(e.target.value)}
                    className="w-full px-3.5 py-2.5 text-xs bg-slate-900 border border-slate-700 rounded-xl text-slate-100 focus:outline-none focus:border-cyan-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1">
                    Your Mobile Number
                  </label>
                  <input
                    type="text"
                    value={victimPhone}
                    onChange={(e) => setVictimPhone(e.target.value)}
                    className="w-full px-3.5 py-2.5 text-xs bg-slate-900 border border-slate-700 rounded-xl text-slate-100 font-mono focus:outline-none focus:border-cyan-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1">
                    State / City
                  </label>
                  <input
                    type="text"
                    value={victimState}
                    onChange={(e) => setVictimState(e.target.value)}
                    className="w-full px-3.5 py-2.5 text-xs bg-slate-900 border border-slate-700 rounded-xl text-slate-100 focus:outline-none focus:border-cyan-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold text-slate-400 mb-1">
                    Targeted / Prevented Amount (₹)
                  </label>
                  <input
                    type="number"
                    value={financialLoss}
                    onChange={(e) => setFinancialLoss(e.target.value)}
                    className="w-full px-3.5 py-2.5 text-xs bg-slate-900 border border-slate-700 rounded-xl text-slate-100 font-mono focus:outline-none focus:border-cyan-500"
                  />
                </div>
              </div>

              {/* Action Button */}
              <button
                onClick={handleGenerateAndSubmit}
                disabled={isSubmitting}
                className="w-full py-3 px-4 rounded-xl font-bold text-xs sm:text-sm bg-rose-600 hover:bg-rose-500 text-white shadow-lg shadow-rose-950/50 transition-colors flex items-center justify-center gap-2 cursor-pointer mt-2"
              >
                {isSubmitting ? (
                  <span>Generating Legal Complaint...</span>
                ) : (
                  <>
                    <FileText className="w-4 h-4" />
                    <span>Generate Structured Cyber Crime Complaint</span>
                  </>
                )}
              </button>
            </>
          ) : (
            /* Complaint Generated View */
            <div className="space-y-4">
              <div className="p-3.5 rounded-xl bg-emerald-950/60 border border-emerald-800/40 text-emerald-200 text-xs flex items-center justify-between">
                <div>
                  <span className="font-bold text-sm block">Complaint Dossier Ready</span>
                  <span className="font-mono text-emerald-300">Complaint ID: {filedReport.complaintId}</span>
                </div>
                <div className="px-2.5 py-1 rounded bg-emerald-900/60 text-emerald-200 font-mono text-[10px] font-bold">
                  DRAFT READY
                </div>
              </div>

              {/* Text Area */}
              <textarea
                readOnly
                rows={10}
                value={filedReport.complaintText}
                className="w-full p-3.5 text-xs bg-slate-950 border border-slate-800 rounded-xl text-slate-200 font-mono leading-relaxed resize-none focus:outline-none"
              />

              {/* Copy / Download / Portal buttons */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                <button
                  onClick={() => handleCopyText(filedReport.complaintText)}
                  className="py-2.5 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold flex items-center justify-center gap-2 cursor-pointer transition-colors"
                >
                  {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4 text-cyan-400" />}
                  <span>{copied ? 'Copied!' : 'Copy Text'}</span>
                </button>

                <button
                  onClick={handleDownloadTxt}
                  className="py-2.5 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold flex items-center justify-center gap-2 cursor-pointer transition-colors"
                >
                  <Download className="w-4 h-4 text-cyan-400" />
                  <span>Download .TXT</span>
                </button>

                <a
                  href="https://cybercrime.gov.in"
                  target="_blank"
                  rel="noreferrer"
                  className="py-2.5 px-3 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 text-xs font-bold flex items-center justify-center gap-2 transition-colors"
                >
                  <ExternalLink className="w-4 h-4" />
                  <span>cybercrime.gov.in</span>
                </a>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
