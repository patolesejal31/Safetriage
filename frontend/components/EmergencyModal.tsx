"use client";

import React from "react";
import { AlertOctagon, PhoneCall, X } from "lucide-react";

interface EmergencyModalProps {
  isOpen: boolean;
  onClose: () => void;
  ruleTitle?: string;
  rationale?: string;
  primaryPhone?: string;
  ambulancePhone?: string;
}

export default function EmergencyModal({
  isOpen,
  onClose,
  ruleTitle,
  rationale,
  primaryPhone = "112",
  ambulancePhone = "108",
}: EmergencyModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/80 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="relative bg-white rounded-2xl max-w-lg w-full border-4 border-red-600 shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        {/* Red Header Bar */}
        <div className="bg-red-600 text-white p-6 flex items-start gap-4">
          <div className="p-3 bg-white/20 rounded-xl shrink-0">
            <AlertOctagon className="w-8 h-8 text-white animate-bounce" />
          </div>
          <div>
            <span className="text-xs font-bold uppercase tracking-widest text-red-100">
              Immediate Warning — Level 1
            </span>
            <h2 className="text-xl font-extrabold text-white">Emergency Medical Alert</h2>
            <p className="text-xs text-red-100 mt-1">
              Potential life-threatening signs detected by clinical safety engine.
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-white/80 hover:text-white p-1 ml-auto rounded-lg hover:bg-white/10"
            aria-label="Close"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-4">
          {ruleTitle && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-sm text-red-900">
              <span className="font-bold">Detected Condition:</span> {ruleTitle}
              {rationale && <p className="text-xs text-red-800 mt-1">{rationale}</p>}
            </div>
          )}

          <div className="space-y-2 text-sm text-slate-700">
            <p className="font-semibold text-slate-900">Recommended Immediate Action:</p>
            <ul className="list-disc pl-5 space-y-1 text-xs text-slate-600">
              <li>Call emergency services immediately or have someone drive you to the nearest emergency room.</li>
              <li>Do not drive yourself if you are feeling faint, dizzy, or experiencing severe pain.</li>
              <li>Rest comfortably in a seated or lying position while waiting for assistance.</li>
            </ul>
          </div>

          {/* Quick Call Box */}
          <div className="bg-slate-900 text-white rounded-xl p-4 flex items-center justify-between">
            <div>
              <p className="text-xs text-slate-400">Call Emergency Help Now</p>
              <p className="text-2xl font-bold tracking-tight text-white">{primaryPhone} / {ambulancePhone}</p>
            </div>
            <a
              href={`tel:${primaryPhone}`}
              className="inline-flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white px-4 py-2.5 rounded-lg text-sm font-bold shadow-md transition-colors"
            >
              <PhoneCall className="w-4 h-4" />
              Call {primaryPhone}
            </a>
          </div>

          <p className="text-[11px] text-slate-400 text-center">
            SafeTriage is an informational academic prototype and cannot dispatch an ambulance.
          </p>

          <button
            onClick={onClose}
            className="w-full py-2.5 px-4 border border-slate-300 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors"
          >
            I Understand — Proceed to Assessment Details
          </button>
        </div>
      </div>
    </div>
  );
}
