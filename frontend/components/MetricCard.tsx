import React from "react";
import { LucideIcon } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  badge?: string;
  variant?: "default" | "success" | "danger" | "warning";
}

export default function MetricCard({
  title,
  value,
  subtitle,
  icon: Icon,
  badge,
  variant = "default",
}: MetricCardProps) {
  const variantStyles = {
    default: "border-slate-200 bg-white text-slate-900",
    success: "border-emerald-200 bg-emerald-50/50 text-emerald-950",
    danger: "border-red-200 bg-red-50/50 text-red-950",
    warning: "border-amber-200 bg-amber-50/50 text-amber-950",
  };

  const iconColors = {
    default: "text-medical-600 bg-medical-50",
    success: "text-emerald-600 bg-emerald-100",
    danger: "text-red-600 bg-red-100",
    warning: "text-amber-600 bg-amber-100",
  };

  return (
    <div className={`p-5 rounded-xl border shadow-xs transition-shadow hover:shadow-md ${variantStyles[variant]}`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">{title}</p>
          <div className="flex items-baseline gap-2 mt-2">
            <span className="text-2xl font-bold tracking-tight">{value}</span>
            {badge && (
              <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 border">
                {badge}
              </span>
            )}
          </div>
          {subtitle && <p className="text-xs text-slate-500 mt-1">{subtitle}</p>}
        </div>
        <div className={`p-2.5 rounded-lg shrink-0 ${iconColors[variant]}`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>
    </div>
  );
}
