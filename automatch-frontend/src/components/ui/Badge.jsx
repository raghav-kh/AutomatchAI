const VARIANTS = {
  primary: "bg-[var(--color-primary-soft)] text-[var(--color-primary)] border border-[var(--color-primary)]/30",
  cyan: "bg-[var(--color-accent-cyan-soft)] text-[var(--color-accent-cyan)] border border-[var(--color-accent-cyan)]/30",
  success: "bg-[var(--color-success-soft)] text-[var(--color-success)] border border-[var(--color-success)]/30",
  warning: "bg-[var(--color-warning-soft)] text-[var(--color-warning)] border border-[var(--color-warning)]/30",
  danger: "bg-[var(--color-danger-soft)] text-[var(--color-danger)] border border-[var(--color-danger)]/30",
  neutral: "bg-[var(--color-surface-subtle)] text-[var(--color-text-muted)] border border-[var(--color-line)]",
};

export default function Badge({ children, variant = "neutral", className = "", icon: Icon }) {
  const variantClass = VARIANTS[variant] || VARIANTS.neutral;
  return (
    <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium ${variantClass} ${className}`}>
      {Icon && <Icon className="w-3.5 h-3.5" aria-hidden="true" />}
      {children}
    </span>
  );
}
