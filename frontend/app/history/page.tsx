"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import {
  History,
  Trash2,
  ExternalLink,
  ShieldAlert,
  RotateCcw,
  CheckCircle,
  AlertTriangle,
  Clock,
  Layers
} from "lucide-react";
import { api } from "@/lib/api";
import { AssessmentListItem } from "@/lib/types";
import { formatIndianTime } from "@/lib/formatTime";
import TriageBadge from "@/components/TriageBadge";

export default function AssessmentHistoryPage() {
  const [historyItems, setHistoryItems] = useState<AssessmentListItem[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [clearing, setClearing] = useState(false);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      const res = await api.listAssessments(100, 0);
      setHistoryItems(res.items);
      setTotal(res.total);
    } catch (err: any) {
      setError(err.message || "Failed to load history.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleDelete = async (id: string) => {
    if (!confirm("Are you sure you want to permanently delete this assessment record?")) return;
    setDeletingId(id);
    try {
      await api.deleteAssessment(id);
      setHistoryItems((prev) => prev.filter((item) => item.id !== id));
      setTotal((prev) => prev - 1);
    } catch (err: any) {
      alert(err.message || "Failed to delete record.");
    } finally {
      setDeletingId(null);
    }
  };

  const handleClearAll = async () => {
    if (!confirm("Are you sure you want to permanently clear all assessment records from local storage? This cannot be undone.")) return;
    setClearing(true);
    try {
      await api.clearAllAssessments();
      setHistoryItems([]);
      setTotal(0);
    } catch (err: any) {
      alert(err.message || "Failed to clear history.");
    } finally {
      setClearing(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-medical-700 text-xs font-bold uppercase tracking-wider mb-1">
            <History className="w-4 h-4" />
            <span>Local Assessment Storage</span>
          </div>
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Assessment History</h1>
          <p className="text-sm text-slate-600 mt-1">
            Manage your saved symptom evaluations stored locally in your SQLite database.
          </p>
        </div>

        {total > 0 && (
          <button
            onClick={handleClearAll}
            disabled={clearing}
            className="inline-flex items-center gap-1.5 text-xs font-semibold text-red-600 hover:text-red-700 border border-red-200 hover:bg-red-50 px-3.5 py-2 rounded-lg transition-colors shadow-2xs"
          >
            <Trash2 className="w-4 h-4" />
            <span>Clear All History</span>
          </button>
        )}
      </div>

      {/* Privacy Guarantee Banner */}
      <div className="rounded-xl border border-slate-200 bg-white p-4 text-xs text-slate-600 flex items-start gap-3">
        <ShieldAlert className="w-5 h-5 text-medical-600 shrink-0 mt-0.5" />
        <div>
          <strong className="text-slate-900">Privacy & Data Minimization:</strong> Assessments are stored in local
          relational tables without personal names, addresses, or phone numbers. Records can be permanently deleted at
          any time using the controls below.
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-xs text-red-800">
          {error}
        </div>
      )}

      {loading ? (
        <div className="py-20 text-center space-y-3">
          <div className="w-8 h-8 border-3 border-medical-600 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-xs text-slate-500 font-medium">Loading assessment records...</p>
        </div>
      ) : historyItems.length === 0 ? (
        <div className="bg-white border border-slate-200 rounded-2xl p-12 text-center space-y-4 shadow-xs">
          <div className="w-12 h-12 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center mx-auto">
            <History className="w-6 h-6" />
          </div>
          <h3 className="text-base font-bold text-slate-900">No Assessment Records Stored</h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            You have not run any symptom assessments yet, or previous history has been cleared.
          </p>
          <Link
            href="/assess"
            className="inline-flex items-center gap-2 px-4 py-2 bg-medical-700 text-white rounded-lg text-xs font-semibold hover:bg-medical-800 transition-colors"
          >
            <span>Start an Assessment</span>
          </Link>
        </div>
      ) : (
        <div className="bg-white border border-slate-200 rounded-2xl shadow-xs overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-xs divide-y divide-slate-200">
              <thead className="bg-slate-50 text-slate-700 font-semibold">
                <tr>
                  <th className="py-3 px-4">Timestamp (IST)</th>
                  <th className="py-3 px-4">Triage Urgency</th>
                  <th className="py-3 px-4">Symptom Summary</th>
                  <th className="py-3 px-4">Age Group</th>
                  <th className="py-3 px-4">Pipeline Mode</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {historyItems.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-3.5 px-4 text-slate-500 whitespace-nowrap font-medium">
                      {formatIndianTime(item.created_at)}
                    </td>
                    <td className="py-3.5 px-4 whitespace-nowrap">
                      <TriageBadge level={item.triage_level} size="sm" />
                    </td>
                    <td className="py-3.5 px-4 text-slate-800 font-medium max-w-xs truncate">
                      {item.symptom_summary}
                    </td>
                    <td className="py-3.5 px-4 text-slate-600 capitalize">
                      {item.user_age_group}
                    </td>
                    <td className="py-3.5 px-4 text-slate-500 font-mono text-[11px]">
                      {item.execution_mode}
                    </td>
                    <td className="py-3.5 px-4 text-right whitespace-nowrap space-x-2">
                      <Link
                        href={`/results/${item.id}`}
                        className="inline-flex items-center gap-1 text-medical-700 hover:text-medical-800 font-semibold px-2 py-1 rounded hover:bg-medical-50"
                      >
                        <span>View</span>
                        <ExternalLink className="w-3.5 h-3.5" />
                      </Link>
                      <button
                        onClick={() => handleDelete(item.id)}
                        disabled={deletingId === item.id}
                        className="inline-flex items-center gap-1 text-red-600 hover:text-red-700 font-semibold px-2 py-1 rounded hover:bg-red-50 disabled:opacity-50"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                        <span>Delete</span>
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
