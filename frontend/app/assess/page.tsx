"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import {
  Stethoscope,
  AlertTriangle,
  Clock,
  RotateCcw,
  Send,
  HelpCircle,
  ShieldAlert,
  Sparkles,
  Info
} from "lucide-react";
import { api } from "@/lib/api";
import { AssessmentRequest, AssessmentResponse, FollowUpQuestion } from "@/lib/types";
import EmergencyModal from "@/components/EmergencyModal";

const EXAMPLE_VIGNETTES = [
  {
    label: "Headache + Vomiting",
    text: "I have had a mild headache since yesterday, and today I started vomiting.",
  },
  {
    label: "Emergency Chest Pain",
    text: "Crushing chest pain radiating down my left arm with severe shortness of breath and sweating.",
  },
  {
    label: "FAST Stroke Signs",
    text: "My mother suddenly cannot move her right arm and her speech is slurred and garbled since 20 minutes ago.",
  },
  {
    label: "Negated Chest Pain (Adversarial)",
    text: "I do NOT have any chest pain, and I do not have difficulty breathing. Just feeling slightly nauseous.",
  },
  {
    label: "Mild Common Cold",
    text: "Mild runny nose, sneezing, and clear nasal discharge for 2 days. No fever, eating normally.",
  },
];

export default function SymptomAssessmentPage() {
  const router = useRouter();

  // Form State
  const [symptomText, setSymptomText] = useState("");
  const [ageGroup, setAgeGroup] = useState("adult");
  const [duration, setDuration] = useState("unknown");
  const [severity, setSeverity] = useState("unknown");
  const [associatedAnswers, setAssociatedAnswers] = useState<Record<string, string>>({});

  // Submission & Interactive Follow-Up State
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pendingFollowUps, setPendingFollowUps] = useState<FollowUpQuestion[]>([]);
  const [intermediateAssessment, setIntermediateAssessment] = useState<AssessmentResponse | null>(null);

  // Emergency Modal State
  const [emergencyModalOpen, setEmergencyModalOpen] = useState(false);
  const [emergencyDetails, setEmergencyDetails] = useState<{ title: string; rationale: string }>({
    title: "",
    rationale: "",
  });

  const handleClear = () => {
    setSymptomText("");
    setAgeGroup("adult");
    setDuration("unknown");
    setSeverity("unknown");
    setAssociatedAnswers({});
    setError(null);
    setPendingFollowUps([]);
    setIntermediateAssessment(null);
  };

  const handleSelectExample = (exampleText: string) => {
    setSymptomText(exampleText);
    setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!symptomText.trim() || symptomText.trim().length < 5) {
      setError("Please describe your symptoms in at least 5 characters.");
      return;
    }

    setLoading(true);
    setError(null);

    const payload: AssessmentRequest = {
      text: symptomText,
      age_group: ageGroup,
      duration: duration !== "unknown" ? duration : undefined,
      severity: severity !== "unknown" ? severity : undefined,
      associated_answers: associatedAnswers,
    };

    try {
      const response = await api.submitAssessment(payload);

      // Check if immediate Level 1 Emergency was detected
      if (response.is_emergency) {
        const topRule = response.triggered_rules[0];
        setEmergencyDetails({
          title: topRule ? topRule.rule_name : "Critical Warning Sign",
          rationale: topRule ? topRule.rationale : response.care_recommendation,
        });
        setEmergencyModalOpen(true);
        // Also save response for navigation once modal is closed
        setIntermediateAssessment(response);
        setLoading(false);
        return;
      }

      // If follow-up questions are needed and not yet answered
      if (response.follow_up_questions && response.follow_up_questions.length > 0 && pendingFollowUps.length === 0) {
        setPendingFollowUps(response.follow_up_questions);
        setIntermediateAssessment(response);
        setLoading(false);
        return;
      }

      // Complete assessment: navigate to results page
      router.push(`/results/${response.id}`);
    } catch (err: any) {
      setError(err.message || "An error occurred while assessing symptoms. Is the backend running?");
      setLoading(false);
    }
  };

  const handleFollowUpAnswer = (questionId: string, answer: string) => {
    setAssociatedAnswers((prev) => ({
      ...prev,
      [questionId]: answer,
    }));
  };

  const handleProceedWithAnswers = async () => {
    setLoading(true);
    const payload: AssessmentRequest = {
      text: symptomText,
      age_group: ageGroup,
      duration: duration !== "unknown" ? duration : undefined,
      severity: severity !== "unknown" ? severity : undefined,
      associated_answers: associatedAnswers,
    };

    try {
      const response = await api.submitAssessment(payload);
      if (response.is_emergency) {
        const topRule = response.triggered_rules[0];
        setEmergencyDetails({
          title: topRule ? topRule.rule_name : "Critical Warning Sign",
          rationale: topRule ? topRule.rationale : response.care_recommendation,
        });
        setEmergencyModalOpen(true);
        setIntermediateAssessment(response);
        setLoading(false);
        return;
      }
      router.push(`/results/${response.id}`);
    } catch (err: any) {
      setError(err.message || "Failed to update assessment with follow-up answers.");
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Emergency Modal */}
      <EmergencyModal
        isOpen={emergencyModalOpen}
        onClose={() => {
          setEmergencyModalOpen(false);
          if (intermediateAssessment) {
            router.push(`/results/${intermediateAssessment.id}`);
          }
        }}
        ruleTitle={emergencyDetails.title}
        rationale={emergencyDetails.rationale}
      />

      {/* Header */}
      <div>
        <div className="flex items-center gap-2 text-medical-700 text-xs font-bold uppercase tracking-wider mb-2">
          <Stethoscope className="w-4 h-4" />
          <span>Clinical Assessment Portal</span>
        </div>
        <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Symptom Assessment</h1>
        <p className="text-sm text-slate-600 mt-1">
          Describe what you are feeling in ordinary words. The deterministic safety engine and NLP pipeline will evaluate urgency and provide guidance.
        </p>
      </div>

      {/* Preset Vignette Selector (For testing / demonstration) */}
      <div className="bg-slate-100/70 border border-slate-200 rounded-xl p-4 space-y-2">
        <div className="flex items-center gap-2 text-xs font-semibold text-slate-700">
          <Sparkles className="w-4 h-4 text-medical-600" />
          <span>Quick Example Scenarios (Click to test):</span>
        </div>
        <div className="flex flex-wrap gap-2">
          {EXAMPLE_VIGNETTES.map((ex, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleSelectExample(ex.text)}
              className="text-xs bg-white hover:bg-medical-50 text-slate-700 hover:text-medical-800 px-3 py-1.5 rounded-lg border border-slate-200 transition-colors shadow-2xs"
            >
              {ex.label}
            </button>
          ))}
        </div>
      </div>

      {/* Main Form */}
      <form onSubmit={handleSubmit} className="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 shadow-xs space-y-6">
        {error && (
          <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-800 text-xs flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-red-600 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold">Validation or Server Error</p>
              <p className="mt-0.5">{error}</p>
            </div>
          </div>
        )}

        {/* Symptom Input */}
        <div className="space-y-2">
          <label htmlFor="symptoms" className="block text-sm font-bold text-slate-900">
            What symptoms are you experiencing? <span className="text-red-500">*</span>
          </label>
          <p className="text-xs text-slate-500">
            Include what started, how it feels, and symptoms you explicitly do <em>not</em> have (e.g., &quot;no chest pain&quot;).
          </p>
          <textarea
            id="symptoms"
            rows={5}
            required
            value={symptomText}
            onChange={(e) => setSymptomText(e.target.value)}
            placeholder="e.g. I have had a severe throbbing headache since this morning, feeling nauseous and vomiting. I do not have a stiff neck or chest pain."
            className="w-full rounded-xl border border-slate-300 p-4 text-sm text-slate-900 focus:outline-hidden focus:ring-2 focus:ring-medical-500 focus:border-transparent transition-all placeholder:text-slate-400"
          />
          <div className="flex justify-between text-xs text-slate-400 px-1">
            <span>Minimum 5 characters</span>
            <span>{symptomText.length} / 2000 characters</span>
          </div>
        </div>

        {/* Context Options Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2 border-t border-slate-100">
          {/* Age Group */}
          <div className="space-y-1.5">
            <label htmlFor="age_group" className="block text-xs font-semibold text-slate-700">
              Age Group
            </label>
            <select
              id="age_group"
              value={ageGroup}
              onChange={(e) => setAgeGroup(e.target.value)}
              className="w-full rounded-lg border border-slate-300 p-2.5 text-xs text-slate-800 bg-white focus:outline-hidden focus:ring-2 focus:ring-medical-500"
            >
              <option value="adult">Adult (18 - 64)</option>
              <option value="infant">Infant (Under 1 year)</option>
              <option value="child">Child (1 - 17 years)</option>
              <option value="elderly">Elderly (65+ years)</option>
              <option value="unknown">Prefer not to say</option>
            </select>
          </div>

          {/* Duration */}
          <div className="space-y-1.5">
            <label htmlFor="duration" className="block text-xs font-semibold text-slate-700">
              Duration
            </label>
            <select
              id="duration"
              value={duration}
              onChange={(e) => setDuration(e.target.value)}
              className="w-full rounded-lg border border-slate-300 p-2.5 text-xs text-slate-800 bg-white focus:outline-hidden focus:ring-2 focus:ring-medical-500"
            >
              <option value="unknown">Not specified / Varies</option>
              <option value="less than 1 hour">Less than 1 hour</option>
              <option value="1 to 6 hours">1 to 6 hours</option>
              <option value="today / 24 hours">Today (Under 24 hours)</option>
              <option value="2 to 3 days">2 to 3 days</option>
              <option value="more than 1 week">More than 1 week</option>
            </select>
          </div>

          {/* Severity */}
          <div className="space-y-1.5">
            <label htmlFor="severity" className="block text-xs font-semibold text-slate-700">
              Subjective Severity
            </label>
            <select
              id="severity"
              value={severity}
              onChange={(e) => setSeverity(e.target.value)}
              className="w-full rounded-lg border border-slate-300 p-2.5 text-xs text-slate-800 bg-white focus:outline-hidden focus:ring-2 focus:ring-medical-500"
            >
              <option value="unknown">Unspecified</option>
              <option value="mild">Mild (Noticeable but does not disrupt tasks)</option>
              <option value="moderate">Moderate (Uncomfortable, affects routine)</option>
              <option value="severe">Severe (Intense, debilitating, or worst ever)</option>
            </select>
          </div>
        </div>

        {/* Dynamic Follow-Up Questions Section */}
        {pendingFollowUps.length > 0 && (
          <div className="bg-medical-50/70 border border-medical-200 rounded-xl p-5 space-y-4 animate-in fade-in">
            <div className="flex items-center gap-2 text-medical-900 font-bold text-sm">
              <HelpCircle className="w-5 h-5 text-medical-700" />
              <span>Targeted Clinical Clarifications</span>
            </div>
            <p className="text-xs text-medical-800">
              The safety engine identified critical qualifiers that help clarify your care level accurately:
            </p>

            <div className="space-y-4 pt-2">
              {pendingFollowUps.map((q) => (
                <div key={q.id} className="bg-white p-3.5 rounded-lg border border-medical-200 space-y-2">
                  <p className="text-xs font-semibold text-slate-900">{q.question}</p>
                  <div className="flex gap-2">
                    {q.options.map((opt) => (
                      <button
                        key={opt}
                        type="button"
                        onClick={() => handleFollowUpAnswer(q.id, opt)}
                        className={`text-xs px-3 py-1.5 rounded-md font-medium border transition-colors ${
                          associatedAnswers[q.id] === opt
                            ? "bg-medical-700 text-white border-medical-700"
                            : "bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100"
                        }`}
                      >
                        {opt}
                      </button>
                    ))}
                  </div>
                  {q.critical_warning_if_yes && associatedAnswers[q.id] === "Yes" && (
                    <p className="text-[11px] text-red-600 font-medium flex items-center gap-1">
                      <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
                      {q.critical_warning_if_yes}
                    </p>
                  )}
                </div>
              ))}
            </div>

            <button
              type="button"
              onClick={handleProceedWithAnswers}
              disabled={loading}
              className="w-full py-2.5 px-4 rounded-lg bg-medical-700 hover:bg-medical-800 text-white font-semibold text-xs shadow-xs transition-colors flex items-center justify-center gap-2"
            >
              <span>Update Assessment with Answers</span>
              <Send className="w-3.5 h-3.5" />
            </button>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-slate-200">
          <button
            type="button"
            onClick={handleClear}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-1.5 text-xs font-medium text-slate-600 hover:text-slate-900 px-4 py-2.5 rounded-lg hover:bg-slate-100 transition-colors"
          >
            <RotateCcw className="w-4 h-4 text-slate-400" />
            <span>Clear Assessment</span>
          </button>

          <button
            type="submit"
            disabled={loading}
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl text-sm font-bold text-white bg-medical-700 hover:bg-medical-800 shadow-md hover:shadow-lg transition-all disabled:opacity-50"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Evaluating Safety Rules...
              </span>
            ) : (
              <>
                <span>Submit for Triage</span>
                <Send className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </form>

      {/* Safety Notice */}
      <div className="text-center text-xs text-slate-400 flex items-center justify-center gap-2">
        <ShieldAlert className="w-4 h-4 text-slate-400" />
        <span>
          Emergency invariant enforced: If acute warning signs are detected, emergency guidance is displayed immediately.
        </span>
      </div>
    </div>
  );
}
