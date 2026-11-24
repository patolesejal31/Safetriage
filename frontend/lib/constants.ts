import { TriageLevel } from "./types";

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const TRIAGE_METADATA: Record<
  TriageLevel,
  {
    name: string;
    description: string;
    timeframe: string;
    badgeClass: string;
    cardBorderClass: string;
    accentBg: string;
    iconName: string;
  }
> = {
  "Level 1": {
    name: "Emergency / Immediate Care",
    description: "Critical, potentially life-threatening symptoms requiring immediate medical evaluation.",
    timeframe: "Immediate (Minutes)",
    badgeClass: "bg-red-100 text-red-800 border-red-300",
    cardBorderClass: "border-red-500 bg-red-50/40",
    accentBg: "bg-red-600 text-white",
    iconName: "AlertTriangle",
  },
  "Level 2": {
    name: "Urgent Medical Attention",
    description: "High-acuity symptoms requiring clinical assessment within hours to prevent deterioration.",
    timeframe: "Within hours (Same day)",
    badgeClass: "bg-amber-100 text-amber-800 border-amber-300",
    cardBorderClass: "border-amber-500 bg-amber-50/40",
    accentBg: "bg-amber-600 text-white",
    iconName: "Clock",
  },
  "Level 3": {
    name: "Routine Medical Consultation",
    description: "Subacute or mild symptoms appropriate for scheduled outpatient primary care appointment.",
    timeframe: "Within 24 to 72 hours",
    badgeClass: "bg-blue-100 text-blue-800 border-blue-300",
    cardBorderClass: "border-blue-400 bg-blue-50/30",
    accentBg: "bg-blue-600 text-white",
    iconName: "Calendar",
  },
  "Level 4": {
    name: "Self-Care Information / Monitoring",
    description: "Mild, self-limiting symptoms suitable for home care, rest, hydration, and monitoring.",
    timeframe: "Monitor over 3 to 5 days",
    badgeClass: "bg-emerald-100 text-emerald-800 border-emerald-300",
    cardBorderClass: "border-emerald-500 bg-emerald-50/30",
    accentBg: "bg-emerald-600 text-white",
    iconName: "ShieldCheck",
  },
};

export const DEFAULT_EMERGENCY_CONTACTS = {
  primary: "112",
  ambulance: "108",
  disclaimer: "SafeTriage is a research prototype. It does not dispatch emergency services or verify hospital availability.",
};
