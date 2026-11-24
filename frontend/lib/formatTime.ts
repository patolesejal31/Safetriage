/**
 * Utility functions for formatting timestamps in Indian Standard Time (IST, UTC+05:30).
 */

export function formatIndianTime(dateInput: string | Date | number | undefined | null): string {
  if (!dateInput) return "N/A";
  const date = typeof dateInput === "string" || typeof dateInput === "number" ? new Date(dateInput) : dateInput;
  if (isNaN(date.getTime())) return "N/A";

  return (
    date.toLocaleString("en-IN", {
      timeZone: "Asia/Kolkata",
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    }) + " IST"
  );
}

export function formatIndianDate(dateInput: string | Date | number | undefined | null): string {
  if (!dateInput) return "N/A";
  const date = typeof dateInput === "string" || typeof dateInput === "number" ? new Date(dateInput) : dateInput;
  if (isNaN(date.getTime())) return "N/A";

  return date.toLocaleDateString("en-IN", {
    timeZone: "Asia/Kolkata",
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}
