"use client";

import React from "react";

interface ConfusionMatrixProps {
  matrix: number[][];
  classes: string[];
}

export default function ConfusionMatrix({ matrix, classes }: ConfusionMatrixProps) {
  if (!matrix || matrix.length === 0) {
    return <div className="text-xs text-slate-400">No confusion matrix data available.</div>;
  }

  // Find max value in matrix for relative color heat-mapping
  const maxVal = Math.max(...matrix.flatMap((row) => row), 1);

  return (
    <div className="overflow-x-auto">
      <div className="inline-block min-w-full align-middle">
        <div className="text-xs font-semibold text-slate-500 mb-2 text-center">
          Predicted Categories (Columns) →
        </div>
        <table className="min-w-full border-collapse border border-slate-200 text-center text-xs">
          <thead>
            <tr className="bg-slate-50">
              <th className="p-2 border border-slate-200 text-left font-bold text-slate-700 w-28">
                Actual Ground Truth ↓
              </th>
              {classes.map((cls) => (
                <th key={cls} className="p-2 border border-slate-200 font-semibold text-slate-700 min-w-20">
                  {cls}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {matrix.map((row, rIdx) => {
              const actualClass = classes[rIdx];
              return (
                <tr key={actualClass}>
                  <td className="p-2 border border-slate-200 text-left font-semibold text-slate-700 bg-slate-50">
                    {actualClass}
                  </td>
                  {row.map((val, cIdx) => {
                    const isDiagonal = rIdx === cIdx;
                    const intensity = val / maxVal;
                    // Color styling: Green tints on diagonal (correct), Red/Orange tints on off-diagonal (errors)
                    let bgStyle = "bg-white";
                    let textColor = "text-slate-800";

                    if (val > 0) {
                      if (isDiagonal) {
                        bgStyle = intensity > 0.5 ? "bg-emerald-600 text-white font-bold" : "bg-emerald-100 text-emerald-900 font-semibold";
                      } else {
                        // Under-triage error: actual is more urgent than pred (cIdx > rIdx)
                        if (cIdx > rIdx) {
                          bgStyle = "bg-red-100 text-red-900 font-semibold";
                        } else {
                          bgStyle = "bg-amber-100 text-amber-900 font-semibold";
                        }
                      }
                    }

                    return (
                      <td
                        key={`${rIdx}-${cIdx}`}
                        className={`p-3 border border-slate-200 transition-colors ${bgStyle} ${textColor}`}
                        title={`Actual: ${actualClass}, Predicted: ${classes[cIdx]} (Count: ${val})`}
                      >
                        {val}
                      </td>
                    );
                  })}
                </tr>
              );
            })}
          </tbody>
        </table>
        <div className="flex items-center justify-between text-[11px] text-slate-500 mt-2 px-1">
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 bg-emerald-500 inline-block rounded-xs"></span>
            <span>Correct Classification (Diagonal)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 bg-red-200 inline-block rounded-xs"></span>
            <span>Under-triage (Dangerous Error)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 bg-amber-200 inline-block rounded-xs"></span>
            <span>Over-triage (Precautionary)</span>
          </div>
        </div>
      </div>
    </div>
  );
}
