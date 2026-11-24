import React from "react";
import { TriageLevel } from "@/lib/types";
import { TRIAGE_METADATA } from "@/lib/constants";
import { AlertTriangle, Clock, Calendar, ShieldCheck } from "lucide-react";

interface TriageBadgeProps {
  level: TriageLevel;
  size?: "sm" | "md" | "lg";
  showDescription?: boolean;
}

export default function TriageBadge({ level, size = "md", showDescription = false }: TriageBadgeProps) {
  const meta = TRIAGE_METADATA[level] || TRIAGE_METADATA["Level 3"];

  const iconMap: Record<string, React.ReactNode> = {
    AlertTriangle: <AlertTriangle className={size === "sm" ? "w-3.5 h-3.5" : size === "lg" ? "w-5 h-5" : "w-4 h-4"} />,
    Clock: <Clock className={size === "sm" ? "w-3.5 h-3.5" : size === "lg" ? "w-5 h-5" : "w-4 h-4"} />,
    Calendar: <Calendar className={size === "sm" ? "w-3.5 h-3.5" : size === "lg" ? "w-5 h-5" : "w-4 h-4"} />,
    ShieldCheck: <ShieldCheck className={size === "sm" ? "w-3.5 h-3.5" : size === "lg" ? "w-5 h-5" : "w-4 h-4"} />,
  };

  const sizeClasses = {
    sm: "px-2 py-0.5 text-xs font-semibold gap-1",
    md: "px-3 py-1.5 text-sm font-semibold gap-1.5",
    lg: "px-4 py-2 text-base font-bold gap-2",
  };

  return (
    <div className="inline-flex flex-col">
      <span
        className={`inline-flex items-center rounded-md border ${meta.badgeClass} ${sizeClasses[size]}`}
      >
        {iconMap[meta.iconName]}
        <span>{level}: {meta.name}</span>
      </span>
      {showDescription && (
        <span className="text-xs text-slate-500 mt-1 font-normal">
          {meta.description} ({meta.timeframe})
        </span>
      )}
    </div>
  );
}
