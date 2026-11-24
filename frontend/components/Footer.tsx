import React from "react";
import Link from "next/link";
import { ShieldCheck, PhoneCall, FileText, ExternalLink } from "lucide-react";

export default function Footer() {
  return (
    <footer className="border-t border-slate-200 bg-slate-50 text-slate-600 text-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          {/* Medical Disclaimer */}
          <div className="md:col-span-2 space-y-3">
            <div className="flex items-center gap-2 text-slate-900 font-semibold">
              <ShieldCheck className="w-5 h-5 text-medical-700" />
              <span>Medical & Research Disclaimer</span>
            </div>
            <p className="text-xs text-slate-500 leading-relaxed">
              SafeTriage is an experimental software framework developed for an MCA research investigation into
              hybrid deterministic safety rules and large language models for medical symptom triage.
              <strong> SafeTriage does not provide medical diagnoses, prescribe pharmaceuticals, or replace clinical consultations.</strong>
              If you or someone in your care experiences severe chest pain, stroke warning signs, acute shortness of breath,
              or loss of consciousness, seek immediate emergency medical care.
            </p>
            <p className="text-xs text-slate-400">
              Deterministic rules are modeled after national clinical guidelines from ICMR, AIIMS New Delhi, MoHFW, and Cardiological Society of India (CSI).
            </p>
          </div>

          {/* Quick links & Emergency help */}
          <div className="space-y-3">
            <div className="flex items-center gap-2 text-slate-900 font-semibold">
              <PhoneCall className="w-5 h-5 text-red-600" />
              <span>Emergency Services (India)</span>
            </div>
            <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-xs text-red-900 space-y-1">
              <div className="font-bold flex justify-between">
                <span>National Emergency & Ambulance:</span>
                <span className="text-base text-red-700">112 / 108</span>
              </div>
              <p className="text-[11px] text-red-800">
                SafeTriage cannot dispatch emergency personnel. Call local emergency numbers directly.
              </p>
            </div>
            <div className="pt-2 flex flex-wrap gap-3 text-xs">
              <Link href="/assess" className="text-medical-700 hover:underline">
                Assess Symptoms
              </Link>
              <span className="text-slate-300">•</span>
              <Link href="/dashboard" className="text-medical-700 hover:underline">
                Research Dashboard
              </Link>
            </div>
          </div>
        </div>

        <div className="border-t border-slate-200 pt-6 flex flex-col sm:flex-row justify-between items-center text-xs text-slate-500 gap-3">
          <p>© {new Date().getFullYear()} SafeTriage Research Project. MCA Academic Dissertation.</p>
          <p className="text-slate-400">
            Local SQLite • Deterministic Rules • Transparent Invariants
          </p>
        </div>
      </div>
    </footer>
  );
}
