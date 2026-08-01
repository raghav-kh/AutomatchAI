import { Loader2 } from "lucide-react";

const VARIANTS = {
  primary: "bg-[var(--color-primary)] text-white hover:bg-[var(--color-primary-hover)] shadow-[var(--shadow-glow-primary)]",
  cyan: "bg-[var(--color-accent-cyan)] text-gray-950 font-semibold hover:bg-cyan-400 shadow-[var(--shadow-glow-cyan)]",
  secondary: "bg-[var(--color-surface-subtle)] text-[var(--color-text-main)] hover:bg-[var(--color-surface-hover)] border border-[var(--color-line)]",
  ghost: "bg-transparent text-[var(--color-text-muted)] hover:text-[var(--color-text-main)] hover:bg-[var(--color-surface-subtle)]",
  danger: "bg-[var(--color-danger)] text-white hover:bg-red-600",
};

const SIZES = {
  sm: "px-3 py-1.5 text-xs rounded-lg gap-1.5",
  md: "px-4 py-2.5 text-sm rounded-xl gap-2",
  lg: "px-6 py-3.5 text-base rounded-xl gap-2.5 font-semibold",
};

export default function Button({
  children,
  variant = "primary",
  size = "md",
  loading = false,
  disabled = false,
  icon: Icon,
  className = "",
  type = "button",
  ...props
}) {
  const variantClass = VARIANTS[variant] || VARIANTS.primary;
  const sizeClass = SIZES[size] || SIZES.md;

  return (
    <button
      type={type}
      disabled={disabled || loading}
      className={`inline-flex items-center justify-center font-medium button-press cursor-pointer transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none ${variantClass} ${sizeClass} ${className}`}
      {...props}
    >
      {loading ? (
        <Loader2 className="w-4 h-4 animate-spin" aria-hidden="true" />
      ) : Icon ? (
        <Icon className="w-4 h-4" aria-hidden="true" />
      ) : null}
      {children}
    </button>
  );
}
