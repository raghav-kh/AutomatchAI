import { Trophy, Check } from "lucide-react";
import Badge from "../ui/Badge";

const ROWS = [
  { key: "price", label: "Ex-Showroom Price", fmt: (v) => (v != null ? `₹${v.toLocaleString("en-IN")}` : "—") },
  { key: "fuel", label: "Fuel Type", fmt: (v) => v ?? "—" },
  { key: "transmission", label: "Transmission", fmt: (v) => v ?? "—" },
  { key: "safety_rating", label: "Safety Rating", fmt: (v) => (v != null ? `${v}/5 Star` : "Unrated"), isHighestBest: true },
  { key: "airbags", label: "Airbags", fmt: (v) => (v != null ? `${v} Airbags` : "—"), isHighestBest: true },
  { key: "mileage", label: "Fuel Mileage", fmt: (v) => (v != null ? `${v} km/l` : "—"), isHighestBest: true },
  { key: "boot_space", label: "Boot Space", fmt: (v) => (v != null ? `${v} Liters` : "—"), isHighestBest: true },
  { key: "ground_clearance", label: "Ground Clearance", fmt: (v) => (v != null ? `${v} mm` : "—"), isHighestBest: true },
  { key: "family_score", label: "Family Fit Score", fmt: (v) => (v != null ? `${v}/10` : "—"), isHighestBest: true },
  { key: "ai_recommendation_score", label: "AI Recommendation Score", fmt: (v) => `${Number(v).toFixed(1)}/10`, isHighestBest: true },
];

export default function CompareMatrix({ rows = [] }) {
  if (!rows || rows.length === 0) return null;

  // Compute winning variant per row (if numerical and highest-is-best)
  const winners = {};
  for (const row of ROWS) {
    if (row.isHighestBest) {
      let maxVal = -Infinity;
      let winnerId = null;
      for (const r of rows) {
        const val = Number(r[row.key]);
        if (!isNaN(val) && val > maxVal) {
          maxVal = val;
          winnerId = r.variant_id;
        }
      }
      if (winnerId != null && maxVal > 0) {
        winners[row.key] = winnerId;
      }
    }
  }

  return (
    <div className="solid-card rounded-2xl border border-[var(--color-line-bright)] overflow-hidden shadow-2xl">
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left border-collapse">
          <thead>
            <tr className="bg-[var(--color-surface-subtle)] border-b border-[var(--color-line)]">
              <th className="p-4 font-display font-semibold text-[var(--color-text-muted)] uppercase tracking-wider text-xs sticky left-0 bg-[var(--color-surface-subtle)] z-10 w-48 border-r border-[var(--color-line)]">
                Specification
              </th>
              {rows.map((r) => (
                <th key={r.variant_id} className="p-4 font-display font-bold text-white min-w-[200px]">
                  <div className="text-xs font-semibold text-cyan-400 uppercase tracking-wider">{r.manufacturer_name}</div>
                  <div className="text-base text-white">{r.car_model}</div>
                  <div className="text-xs text-[var(--color-text-muted)] font-normal">{r.variant_name}</div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-[var(--color-line)]">
            {ROWS.map((row) => (
              <tr key={row.key} className="hover:bg-white/[0.02] transition-colors">
                <td className="p-4 font-medium text-[var(--color-text-muted)] text-xs sticky left-0 bg-[var(--color-surface-solid)] z-10 border-r border-[var(--color-line)]">
                  {row.label}
                </td>
                {rows.map((r) => {
                  const isWinner = winners[row.key] === r.variant_id;
                  const value = r[row.key];
                  const formatted = row.fmt(value);

                  return (
                    <td key={r.variant_id} className={`p-4 font-mono text-sm ${isWinner ? 'text-emerald-400 font-bold bg-emerald-500/5' : 'text-white'}`}>
                      <div className="flex items-center gap-1.5">
                        {formatted}
                        {isWinner && (
                          <span className="inline-flex items-center gap-1 text-[10px] font-sans font-semibold bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded-full border border-emerald-500/30">
                            <Trophy className="w-3 h-3" /> Best
                          </span>
                        )}
                      </div>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
