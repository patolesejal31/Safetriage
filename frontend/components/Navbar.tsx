"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  Activity,
  BarChart2,
  History,
  Stethoscope,
  AlertTriangle,
  LogIn,
  UserPlus,
  LogOut,
  User as UserIcon,
} from "lucide-react";
import { api } from "@/lib/api";
import { User } from "@/lib/types";

export default function Navbar() {
  const pathname = usePathname();
  const [isBackendHealthy, setIsBackendHealthy] = useState<boolean | null>(null);
  const [currentUser, setCurrentUser] = useState<User | null>(null);

  useEffect(() => {
    // Health check
    api.getHealth()
      .then(() => setIsBackendHealthy(true))
      .catch(() => setIsBackendHealthy(false));

    // Load active session
    const syncUser = () => {
      setCurrentUser(api.getCurrentUser());
    };
    syncUser();

    // Verify token with backend if stored
    if (api.isAuthenticated()) {
      api.getMe()
        .then((user) => setCurrentUser(user))
        .catch(() => {
          api.clearSession();
          setCurrentUser(null);
        });
    }

    window.addEventListener("auth-change", syncUser);
    return () => window.removeEventListener("auth-change", syncUser);
  }, []);

  const handleLogout = async () => {
    await api.logout();
    setCurrentUser(null);
  };

  const navLinks = [
    { href: "/assess", label: "Assess Symptoms", icon: Stethoscope },
    { href: "/history", label: "History", icon: History },
    { href: "/dashboard", label: "Research Dashboard", icon: BarChart2 },
  ];

  return (
    <header className="border-b border-slate-200 bg-white sticky top-0 z-40 shadow-xs">
      {/* Top micro-bar for clinical research awareness in Indian Context */}
      <div className="bg-slate-900 text-slate-300 text-xs py-1.5 px-4 text-center flex items-center justify-center gap-2">
        <AlertTriangle className="w-3.5 h-3.5 text-amber-400 shrink-0" />
        <span>
          <strong>Research Prototype (India):</strong> SafeTriage is an investigational framework. In a medical emergency in India, call <strong>112 / 108</strong> immediately.
        </span>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="w-10 h-10 rounded-lg bg-medical-700 flex items-center justify-center text-white shadow-sm group-hover:bg-medical-800 transition-colors">
              <Activity className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="font-bold text-lg text-slate-900 tracking-tight">SafeTriage</span>
                <span className="text-[10px] font-semibold tracking-wider uppercase px-1.5 py-0.5 rounded bg-medical-100 text-medical-800 border border-medical-200">
                  India • Research
                </span>
              </div>
              <p className="text-xs text-slate-500 font-medium">Hybrid NLP & Safety Engine (IST)</p>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => {
              const Icon = link.icon;
              const isActive = pathname === link.href;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`flex items-center gap-1.5 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive
                      ? "bg-medical-50 text-medical-700 border border-medical-200"
                      : "text-slate-600 hover:text-slate-900 hover:bg-slate-50"
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? "text-medical-600" : "text-slate-400"}`} />
                  {link.label}
                </Link>
              );
            })}
          </nav>

          {/* User Auth & Actions */}
          <div className="flex items-center gap-2.5">
            {/* Backend Status indicator */}
            <div className="hidden xl:flex items-center gap-2 px-2.5 py-1 rounded-full text-xs font-medium border bg-slate-50">
              <span
                className={`w-2 h-2 rounded-full ${
                  isBackendHealthy === true
                    ? "bg-emerald-500 ring-2 ring-emerald-200"
                    : isBackendHealthy === false
                    ? "bg-red-500"
                    : "bg-amber-400 animate-pulse"
                }`}
              />
              <span className="text-slate-600">
                {isBackendHealthy === true ? "Engine Active (IST)" : "Connecting..."}
              </span>
            </div>

            {/* Auth Buttons */}
            {currentUser ? (
              <div className="flex items-center gap-2">
                <div className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-100 border border-slate-200 text-xs">
                  <UserIcon className="w-3.5 h-3.5 text-medical-700" />
                  <span className="font-bold text-slate-800 max-w-[120px] truncate">
                    {currentUser.full_name}
                  </span>
                  <span className="text-[10px] uppercase font-semibold px-1 py-0.2 bg-medical-200 text-medical-900 rounded">
                    {currentUser.role}
                  </span>
                </div>
                <button
                  onClick={handleLogout}
                  title="Sign Out"
                  className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg border border-slate-200 text-xs font-semibold text-slate-600 hover:bg-slate-100 hover:text-red-700 transition-colors"
                >
                  <LogOut className="w-3.5 h-3.5" />
                  <span className="hidden sm:inline">Sign Out</span>
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-1.5">
                <Link
                  href="/login"
                  className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors"
                >
                  <LogIn className="w-3.5 h-3.5 text-slate-500" />
                  <span>Sign In</span>
                </Link>
                <Link
                  href="/register"
                  className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-medical-50 border border-medical-200 text-xs font-semibold text-medical-800 hover:bg-medical-100 transition-colors"
                >
                  <UserPlus className="w-3.5 h-3.5 text-medical-600" />
                  <span>Register</span>
                </Link>
              </div>
            )}

            <Link
              href="/assess"
              className="inline-flex items-center justify-center px-3.5 py-1.5 border border-transparent text-xs font-bold rounded-lg shadow-xs text-white bg-medical-700 hover:bg-medical-800 transition-colors"
            >
              Assess
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}
