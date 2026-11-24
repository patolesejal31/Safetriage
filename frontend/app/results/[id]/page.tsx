"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import {
  AlertTriangle,
  ArrowLeft,
  CheckCircle2,
  Clock,
  HelpCircle,
  PhoneCall,
  Printer,
  RotateCcw,
  ShieldAlert,
  ShieldCheck,
  Stethoscope,
  XCircle,
  BookOpen
} from "lucide-react";
import { api } from "@/lib/api";
import { AssessmentResponse } from "@/lib/types";
import { TRIAGE_METADATA } from "@/lib/constants";
import { formatIndianTime } from "@/lib/formatTime";
import TriageBadge from "@/components/TriageBadge";

export default function AssessmentResultsPage() {
  const params = useParams();
  const router = useRouter();
  const id = params?.id as string;

  const [assessment, setAssessment] = useState<AssessmentResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!id) return;
    api.getAssessment(id)
      .then((data) => {
        setAssessment(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || "Could not retrieve assessment record.");
        setLoading(false);
      });
  }, [id]);

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-20 text-center space-y-4">
        <div className="w-10 h-10 border-3 border-medical-600 border-t-transparent rounded-full animate-spin mx-auto" />
        <p className="text-sm text-slate-600 font-medium">Retrieving verified clinical triage result...</p>
      </div>
    );
  }

  if (error || !assessment) {
    return (
      <div className="max-w-xl mx-auto px-4 py-16 text-center space-y-4">
        <div className="w-12 h-12 bg-red-100 text-red-600 rounded-full flex items-center justify-center mx-auto">
          <AlertTriangle className="w-6 h-6" />
        </div>
        <h2 className="text-xl font-bold text-slate-900">Assessment Record Not Found</h2>
        <p className="text-xs text-slate-500">{error || "The requested assessment ID is not available in local records."}</p>
        <Link
          href="/assess"
          className="inline-flex items-center gap-2 px-4 py-2 bg-medical-700 text-white rounded-lg text-xs font-semibold hover:bg-medical-800"
        >
          <RotateCcw className="w-4 h-4" />
          <span>Start a New Assessment</span>
        </Link>
      </div>
    );
  }

  const meta = TRIAGE_METADATA[assessment.triage_level] || TRIAGE_METADATA["Level 3"];
  const isL1 = assessment.triage_level === "Level 1";

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Top Action Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-200 pb-4">
        <Link
          href="/assess"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-600 hover:text-slate-900"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Assessment Input</span>
        </Link>

        <div className="flex items-center gap-3">
          <button
            onClick={() => window.print()}
            className="inline-flex items-center gap-1 text-xs font-medium text-slate-600 hover:text-slate-900 px-3 py-1.5 rounded-md border border-slate-200 hover:bg-slate-50"
          >
            <Printer className="w-3.5 h-3.5" />
            <span>Print Report</span>
          </button>
          <Link
            href="/assess"
            className="inline-flex items-center gap-1.5 text-xs font-bold text-white bg-medical-700 hover:bg-medical-800 px-3.5 py-1.5 rounded-lg shadow-xs"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>New Assessment</span>
          </Link>
        </div>
      </div>

      {/* Primary Triage Category Banner */}
      <div className={`rounded-2xl border-2 p-6 sm:p-8 space-y-6 ${meta.cardBorderClass} shadow-xs`}>
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Assigned Urgency Category
            </span>
            <div className="mt-1">
              <TriageBadge level={assessment.triage_level} size="lg" />
            </div>
          </div>

          <div className="bg-white/80 border border-slate-200 px-4 py-2.5 rounded-xl text-right">
            <span className="text-[11px] font-semibold text-slate-500 block">Recommended Action Window</span>
            <span className="text-sm font-bold text-slate-900 flex items-center gap-1.5 justify-end">
              <Clock className="w-4 h-4 text-slate-500" />
              {assessment.action_timeframe}
            </span>
          </div>
        </div>

        {/* Recommended Action Box */}
        <div className="bg-white rounded-xl p-5 border border-slate-200/80 space-y-2">
          <p className="text-xs font-bold text-slate-500 uppercase tracking-wider">Recommended Next Step:</p>
          <p className="text-base font-extrabold text-slate-900">{assessment.care_recommendation}</p>
        </div>

        {/* Emergency Assistance Hotline (Highlighted if Level 1) */}
        {isL1 && (
          <div className="bg-red-600 text-white rounded-xl p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 shadow-md">
            <div className="space-y-1">
              <div className="flex items-center gap-2 font-bold text-base">
                <AlertTriangle className="w-5 h-5 text-white animate-pulse" />
                <span>Emergency Services Required</span>
              </div>
              <p className="text-xs text-red-100">
                Call {assessment.emergency_contacts?.primary || "112"} or ambulance {assessment.emergency_contacts?.ambulance || "108"} immediately.
              </p>
            </div>
            <a
              href={`tel:${assessment.emergency_contacts?.primary || "112"}`}
              className="inline-flex items-center gap-2 bg-white text-red-700 hover:bg-red-50 font-bold px-4 py-2 rounded-lg text-sm shrink-0 transition-colors"
            >
              <PhoneCall className="w-4 h-4" />
              Call Now
            </a>
          </div>
        )}
      </div>

      {/* Uncertainty Notice (if flagged) */}
      {assessment.uncertainty_flag && (
        <div className="bg-amber-50 border border-amber-300 rounded-xl p-4 text-xs text-amber-900 flex items-start gap-3">
          <HelpCircle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
          <div>
            <strong className="block text-sm">Explicit Uncertainty State</strong>
            <p className="mt-0.5">
              Input descriptions contained ambiguous or unsupported terms. SafeTriage adheres to the safety invariant
              that <em>absence of detected red flags does not confirm safety</em>. An in-person consultation is advised.
            </p>
          </div>
        </div>
      )}

      {/* Structured Symptoms Breakdown */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 space-y-4">
        <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
          <Stethoscope className="w-5 h-5 text-medical-700" />
          <span>Structured Clinical Findings</span>
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          {/* Positive Symptoms */}
          <div className="border border-slate-200 rounded-xl p-4 space-y-2 bg-slate-50/50">
            <span className="font-bold text-slate-700 flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>Recognized Positive Symptoms</span>
            </span>
            {assessment.symptoms && assessment.symptoms.length > 0 ? (
              <ul className="space-y-1.5 pt-1">
                {assessment.symptoms.map((s, idx) => (
                  <li key={idx} className="flex items-center justify-between bg-white px-2.5 py-1.5 rounded border border-slate-200">
                    <span className="font-semibold text-slate-800 capitalize">{s.name}</span>
                    <span className="text-[11px] text-slate-500">{s.severity !== "unknown" ? s.severity : "standard"}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-slate-400 italic">No specific canonical symptoms recognized.</p>
            )}
          </div>

          {/* Negated Symptoms */}
          <div className="border border-slate-200 rounded-xl p-4 space-y-2 bg-slate-50/50">
            <span className="font-bold text-slate-700 flex items-center gap-1.5">
              <XCircle className="w-4 h-4 text-slate-400" />
              <span>Explicitly Denied (Negated) Symptoms</span>
            </span>
            {assessment.negated_symptoms && assessment.negated_symptoms.length > 0 ? (
              <ul className="space-y-1.5 pt-1">
                {assessment.negated_symptoms.map((neg, idx) => (
                  <li key={idx} className="flex items-center gap-1.5 bg-white px-2.5 py-1.5 rounded border border-slate-200 text-slate-600">
                    <span className="line-through text-slate-400">{neg}</span>
                    <span className="text-[10px] bg-slate-100 text-slate-500 px-1.5 py-0.5 rounded font-mono">DENIED</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-slate-400 italic">No negated symptoms stated.</p>
            )}
          </div>
        </div>
      </div>

      {/* Triggered Deterministic Rules */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 space-y-4">
        <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
          <BookOpen className="w-5 h-5 text-medical-700" />
          <span>Triggered Deterministic Safety Rules</span>
        </h3>

        {assessment.triggered_rules && assessment.triggered_rules.length > 0 ? (
          <div className="space-y-3">
            {assessment.triggered_rules.map((rule) => (
              <div key={rule.rule_id} className="border border-slate-200 rounded-xl p-4 bg-slate-50/50 space-y-1 text-xs">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-900 text-sm">
                    {rule.rule_id}: {rule.rule_name}
                  </span>
                  <span className="font-mono text-[10px] px-2 py-0.5 rounded bg-slate-200 text-slate-700">
                    {rule.assigned_level}
                  </span>
                </div>
                <p className="text-slate-600">{rule.rationale}</p>
                <p className="text-[11px] text-slate-400 pt-1">
                  <strong>Clinical Source:</strong> {rule.source_guideline}
                </p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-500 italic">
            No acute red-flag safety rules triggered. Baseline conservative recommendations applied.
          </p>
        )}
      </div>

      {/* Explainable Decision Rationale */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 space-y-3">
        <h3 className="text-base font-bold text-slate-900">Explainable Decision Factors</h3>
        <div className="text-xs text-slate-700 whitespace-pre-line leading-relaxed bg-slate-50 p-4 rounded-xl border border-slate-200 font-mono">
          {assessment.explanation}
        </div>
      </div>

      {/* Limitations and Medical Disclaimer */}
      <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6 space-y-2 text-xs text-slate-500">
        <div className="flex items-center gap-2 text-slate-700 font-bold">
          <ShieldAlert className="w-4 h-4 text-slate-500" />
          <span>Prototype Limitations</span>
        </div>
        <p className="leading-relaxed">{assessment.limitations}</p>
        <div className="pt-2 flex flex-col sm:flex-row sm:items-center justify-between text-[11px] text-slate-400 border-t border-slate-200/60 mt-3 gap-1">
          <span>Assessment ID: {assessment.id}</span>
          <span>Timestamp: {formatIndianTime(assessment.created_at)}</span>
          <span>Pipeline Latency: {assessment.latency_ms} ms</span>
        </div>
      </div>
    </div>
  );
}
