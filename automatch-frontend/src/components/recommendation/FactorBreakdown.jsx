const FACTOR_LABELS = {
  budget_score: "Budget Fit",
  safety_score: "Safety Rating",
  family_score: "Family Fit",
  city_friendliness: "City Friendliness",
  highway_comfort: "Highway Comfort",
  maintenance_score: "Maintenance Level",
  resale_value: "Resale Value",
  service_network: "Service Network",
  fuel_match: "Fuel & Transmission Match",
  parking_fit: "Parking Fit",
};

export default function FactorBreakdown({ breakdown = {} }) {
  const items = Object.entries(breakdown).filter(([_, v]) => v != null);

  if (items.length === 0) return null;

  return (
    <div className="space-y-3 pt-2">
      <h4 className="text-xs font-semibold text-[var(--color-text-muted)] uppercase tracking-wider">
        11-Factor Score Breakdown
      </h4>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-2.5">
        {items.map(([key, score]) => {
          const label = FACTOR_LABELS[key] || key.replace(/_/g, " ");
          const normalized = Math.min(Math.max(Number(score) || 0, 0), 10);
          const percent = (normalized / 10) * 100;

          let colorClass = "bg-indigo-500";
          if (normalized >= 8) colorClass = "bg-emerald-500";
          else if (normalized < 5) colorClass = "bg-amber-500";

          return (
            <div key={key} className="space-y-1">
              <div className="flex justify-between items-center text-xs">
                <span className="text-[var(--color-text-muted)] capitalize">{label}</span>
                <span className="font-mono text-white font-medium">{normalized.toFixed(1)}/10</span>
              </div>
              <div className="h-1.5 w-full bg-[var(--color-surface-subtle)] rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${colorClass}`}
                  style={{ width: `${percent}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
