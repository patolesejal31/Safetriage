import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        medical: {
          50: "#f0f7ff",
          100: "#e0effe",
          200: "#bae0fd",
          300: "#7cc7fb",
          400: "#36abf7",
          500: "#0c8ee9",
          600: "#0271c7",
          700: "#035aa1",
          800: "#074c85",
          900: "#0b406e",
          950: "#072849",
        },
        triage: {
          emergency: "#dc2626", // Level 1
          urgent: "#d97706",    // Level 2
          routine: "#2563eb",   // Level 3
          selfcare: "#059669",  // Level 4
        }
      },
    },
  },
  plugins: [],
};
export default config;
