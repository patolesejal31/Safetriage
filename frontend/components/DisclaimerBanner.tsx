import React from "react";
import { AlertCircle } from "lucide-react";

export default function DisclaimerBanner() {
  return (
    <div className="bg-amber-50 border-b border-amber-200 px-4 py-2.5 text-xs text-amber-900">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-amber-600 shrink-0" />
          <span>
            <strong>Research Prototype Notice:</strong> SafeTriage evaluates preliminary urgency categories. It is not an authorized diagnostic device or doctor replacement.
          </span>
        </div>
        <span className="hidden sm:inline-block text-[11px] font-semibold text-amber-800 bg-amber-100 px-2 py-0.5 rounded border border-amber-300">
          Non-Clinical Prototype
        </span>
      </div>
    </div>
  );
}
