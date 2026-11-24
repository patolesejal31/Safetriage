import React from "react";
import Link from "next/link";
import {
  ShieldAlert,
  Activity,
  ArrowRight,
  Brain,
  Cpu,
  FileCheck2,
  Stethoscope,
  Lock,
  BookOpen,
  FlaskConical,
  Scale,
  BarChart
} from "lucide-react";
import DisclaimerBanner from "@/components/DisclaimerBanner";

export default function LandingPage() {
  return (
    <div className="space-y-16 pb-16">
      <DisclaimerBanner />

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 md:pt-12">
        <div className="max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-medical-50 border border-medical-200 text-medical-800 text-xs font-semibold mb-6">
            <FlaskConical className="w-3.5 h-3.5 text-medical-600" />
            <span>MCA Research Dissertation Project</span>
          </div>

          <h1 className="text-4xl sm:text-5xl font-extrabold text-slate-900 tracking-tight leading-tight">
            Safe & Explainable Medical Symptom Triage
          </h1>

          <p className="mt-4 text-lg text-slate-600 leading-relaxed">
            An investigational hybrid framework pairing <strong>natural language processing</strong> and
            <strong> large language models</strong> with an <strong>independent deterministic clinical safety engine</strong>.
            Designed to ensure AI fluency without permitting unconstrained models to compromise triage safety.
          </p>

          <div className="mt-8 flex flex-wrap items-center gap-4">
            <Link
              href="/assess"
              className="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl text-base font-bold text-white bg-medical-700 hover:bg-medical-800 shadow-md hover:shadow-lg transition-all"
            >
              <Stethoscope className="w-5 h-5" />
              <span>Start Symptom Assessment</span>
              <ArrowRight className="w-4 h-4 ml-1" />
            </Link>

            <Link
              href="/dashboard"
              className="inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl text-base font-semibold text-slate-700 bg-white border border-slate-300 hover:bg-slate-50 transition-colors shadow-xs"
            >
              <BarChart className="w-5 h-5 text-medical-600" />
              <span>Research Dashboard</span>
            </Link>
          </div>

          <div className="mt-8 flex items-center gap-6 text-xs text-slate-500 font-medium border-t border-slate-200 pt-6">
            <div className="flex items-center gap-1.5">
              <Lock className="w-4 h-4 text-emerald-600" />
              <span>Zero Personal Health Identifiers Stored</span>
            </div>
            <div className="flex items-center gap-1.5">
              <Cpu className="w-4 h-4 text-medical-600" />
              <span>100% Offline Rule Execution</span>
            </div>
          </div>
        </div>
      </section>

      {/* 3-Step Clinical Pipeline Workflow */}
      <section className="bg-white border-y border-slate-200 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              Three-Step Triage Pipeline
            </h2>
            <p className="mt-2 text-sm text-slate-600">
              How SafeTriage combines conversational NLP with deterministic safety guarantees.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Step 1 */}
            <div className="relative p-6 rounded-2xl border border-slate-200 bg-slate-50/50 hover:bg-slate-50 transition-colors">
              <div className="w-10 h-10 rounded-xl bg-medical-100 border border-medical-200 flex items-center justify-center text-medical-700 font-bold mb-4">
                1
              </div>
              <h3 className="text-lg font-bold text-slate-900">Describe Symptoms</h3>
              <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                Enter your symptoms in ordinary natural language. The system extracts canonical symptoms, distinguishes
                negations (e.g. <em>&quot;no chest pain&quot;</em>), captures duration, and flags ambiguities.
              </p>
            </div>

            {/* Step 2 */}
            <div className="relative p-6 rounded-2xl border border-slate-200 bg-slate-50/50 hover:bg-slate-50 transition-colors">
              <div className="w-10 h-10 rounded-xl bg-red-100 border border-red-200 flex items-center justify-center text-red-700 font-bold mb-4">
                2
              </div>
              <h3 className="text-lg font-bold text-slate-900">Deterministic Safety Gate</h3>
              <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                Emergency rules evaluate life-threatening danger signs (e.g., FAST stroke criteria, ACS indicators).
                An unconstrained LLM or ML classifier is <strong>never permitted to downgrade an emergency</strong>.
              </p>
            </div>

            {/* Step 3 */}
            <div className="relative p-6 rounded-2xl border border-slate-200 bg-slate-50/50 hover:bg-slate-50 transition-colors">
              <div className="w-10 h-10 rounded-xl bg-emerald-100 border border-emerald-200 flex items-center justify-center text-emerald-700 font-bold mb-4">
                3
              </div>
              <h3 className="text-lg font-bold text-slate-900">Explainable Care Guidance</h3>
              <p className="mt-2 text-xs text-slate-600 leading-relaxed">
                Receive an ordinal urgency classification (Level 1 to 4), recommended action timeframe,
                itemized safety rules triggered, and a transparent, patient-friendly explanation.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Research Framework & Objectives */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-md bg-slate-100 text-slate-700 text-xs font-semibold mb-4">
              <Scale className="w-3.5 h-3.5" />
              <span>Research Methodology</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              Investigating Hybrid Clinical Safety in Healthcare AI
            </h2>
            <p className="mt-4 text-sm text-slate-600 leading-relaxed">
              Standalone Large Language Models demonstrate impressive natural-language parsing, but suffer from
              stochastic hallucination, lack of deterministic reproducibility, and uncalibrated risk scoring.
              Conversely, pure keyword rules struggle with conversational variance.
            </p>
            <p className="mt-3 text-sm text-slate-600 leading-relaxed">
              SafeTriage proposes and evaluates a hybrid architecture that pairs deterministic clinical decision trees
              (grounded in ICMR, AIIMS, and CSI protocols) with modern NLP. The research dashboard allows empirical comparison
              across <strong>Rule-Based</strong>, <strong>scikit-learn ML</strong>, <strong>LLM-Only</strong>, and
              <strong> Proposed Hybrid</strong> models on identical synthetic vignettes.
            </p>
            <div className="mt-6 flex gap-4">
              <Link
                href="/dashboard"
                className="inline-flex items-center text-sm font-semibold text-medical-700 hover:text-medical-800"
              >
                <span>View Research Analytics & Split Architecture</span>
                <ArrowRight className="w-4 h-4 ml-1" />
              </Link>
            </div>
          </div>

          <div className="bg-slate-900 text-slate-100 rounded-2xl p-6 sm:p-8 space-y-6 shadow-xl">
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Brain className="w-5 h-5 text-medical-400" />
              <span>Core System Safety Invariants</span>
            </h3>
            <ul className="space-y-4 text-xs text-slate-300">
              <li className="flex items-start gap-3">
                <span className="w-5 h-5 rounded-full bg-red-900/60 text-red-300 flex items-center justify-center shrink-0 font-bold">1</span>
                <div>
                  <strong className="text-white">Emergency Precedence:</strong> Level 1 danger signs halt standard flows and display emergency warnings without awaiting LLM generation.
                </div>
              </li>
              <li className="flex items-start gap-3">
                <span className="w-5 h-5 rounded-full bg-red-900/60 text-red-300 flex items-center justify-center shrink-0 font-bold">2</span>
                <div>
                  <strong className="text-white">Strict Non-Downgrade Invariant:</strong> Model outputs cannot downgrade an emergency or urgent tier assigned by the deterministic rule engine.
                </div>
              </li>
              <li className="flex items-start gap-3">
                <span className="w-5 h-5 rounded-full bg-red-900/60 text-red-300 flex items-center justify-center shrink-0 font-bold">3</span>
                <div>
                  <strong className="text-white">Explicit Uncertainty State:</strong> Unrecognized input is flagged as uncertain and safely escalated rather than falsely reassuring.
                </div>
              </li>
              <li className="flex items-start gap-3">
                <span className="w-5 h-5 rounded-full bg-red-900/60 text-red-300 flex items-center justify-center shrink-0 font-bold">4</span>
                <div>
                  <strong className="text-white">Zero Key Offline Resilience:</strong> Complete application works locally without external internet access or commercial API keys.
                </div>
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* Privacy & Safety Statement */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 space-y-4">
          <div className="flex items-center gap-2 text-slate-900 font-bold">
            <Lock className="w-5 h-5 text-slate-700" />
            <h3 className="text-base">Privacy & Ethical Disclosure</h3>
          </div>
          <p className="text-xs text-slate-600 leading-relaxed">
            SafeTriage does not require user registration, telephone numbers, emails, or personal identification.
            All assessment history is stored locally in your SQLite database. You can inspect your records and
            permanently delete them at any time from the History page. If you configure an external LLM API key,
            sanitized symptom text is forwarded for explanation generation; otherwise, all processing occurs 100% locally.
          </p>
        </div>
      </section>
    </div>
  );
}
