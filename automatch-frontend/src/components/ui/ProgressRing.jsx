export default function ProgressRing({
  value = 0,
  max = 10,
  size = 64,
  strokeWidth = 6,
  label = "",
  sublabel = "",
  color = "var(--color-primary)",
  className = "",
}) {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const percentage = Math.min(Math.max(value / max, 0), 1);
  const strokeDashoffset = circumference - percentage * circumference;

  return (
    <div className={`relative inline-flex items-center justify-center ${className}`}>
      <svg width={size} height={size} className="transform -rotate-90">
        {/* Background Track */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="var(--color-surface-subtle)"
          strokeWidth={strokeWidth}
          fill="transparent"
        />
        {/* Animated Progress Ring */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={color}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          fill="transparent"
          style={{
            transition: "stroke-dashoffset 800ms cubic-bezier(0.34, 1.56, 0.64, 1)",
          }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
        <span className="font-display font-bold text-sm md:text-base text-[var(--color-text-main)]">
          {label || value}
        </span>
        {sublabel && <span className="text-[10px] text-[var(--color-text-dim)] uppercase tracking-wider">{sublabel}</span>}
      </div>
    </div>
  );
}
