/**
 * The app's signature visual: a semicircular gauge, like a speedometer
 * readout, used everywhere a confidence/quality percentage is shown.
 * Uses SVG's `pathLength` normalization so the dasharray math is just
 * "value out of 100" regardless of the actual arc geometry.
 */
function tierColor(value) {
  if (value >= 70) return "var(--color-accent)";
  if (value >= 40) return "var(--color-caution)";
  return "var(--color-danger)";
}

export default function ConfidenceGauge({ value, label = "confidence", size = 88 }) {
  const clamped = Math.max(0, Math.min(100, value));
  const arcD = "M 10 46 A 36 36 0 0 1 82 46";

  return (
    <div className="flex flex-col items-center" style={{ width: size }}>
      <svg viewBox="0 0 92 52" width={size} height={(size * 52) / 92} aria-hidden="true">
        <path d={arcD} fill="none" stroke="var(--color-line)" strokeWidth="7" strokeLinecap="round" pathLength="100" />
        <path
          d={arcD}
          fill="none"
          stroke={tierColor(clamped)}
          strokeWidth="7"
          strokeLinecap="round"
          pathLength="100"
          strokeDasharray={`${clamped} 100`}
        />
      </svg>
      <div className="-mt-3 font-data font-semibold text-lg" style={{ color: tierColor(clamped) }}>
        {Math.round(clamped)}%
      </div>
      <div className="text-[11px] uppercase tracking-wide text-ink-soft">{label}</div>
    </div>
  );
}
