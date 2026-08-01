const LABELS = {
  budget_fit: "Budget fit",
  safety: "Safety",
  family_fit: "Family fit",
  city_comfort: "City comfort",
  highway_comfort: "Highway comfort",
  maintenance: "Maintenance",
  resale_value: "Resale value",
  service_network: "Service network",
  fuel_match: "Fuel match",
  transmission_match: "Transmission match",
  parking_fit: "Parking fit",
};

export default function ScoreBar({ componentKey, value }) {
  const pct = Math.max(0, Math.min(100, (value / 10) * 100));
  const color = value >= 8 ? "var(--color-accent)" : value <= 4.5 ? "var(--color-caution)" : "var(--color-primary)";

  return (
    <div className="flex items-center gap-3 text-sm">
      <div className="w-36 shrink-0 text-ink-soft">{LABELS[componentKey] ?? componentKey}</div>
      <div className="flex-1 h-2 rounded-full bg-line overflow-hidden">
        <div className="h-full rounded-full" style={{ width: `${pct}%`, background: color }} />
      </div>
      <div className="w-10 shrink-0 text-right font-data text-xs text-ink-soft">{value.toFixed(1)}</div>
    </div>
  );
}
