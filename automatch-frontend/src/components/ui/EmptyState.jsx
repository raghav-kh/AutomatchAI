import { SearchX } from "lucide-react";

export default function EmptyState({
  title = "No results found",
  description = "Try adjusting your filters or search criteria.",
  action = null,
  icon: Icon = SearchX,
  className = "",
}) {
  return (
    <div className={`solid-card rounded-2xl p-8 text-center flex flex-col items-center justify-center border border-[var(--color-line)] ${className}`}>
      <div className="w-14 h-14 rounded-2xl bg-[var(--color-surface-subtle)] text-[var(--color-text-muted)] flex items-center justify-center mb-4">
        <Icon className="w-7 h-7" aria-hidden="true" />
      </div>
      <h3 className="text-lg font-semibold font-display text-[var(--color-text-main)] mb-1">
        {title}
      </h3>
      <p className="text-sm text-[var(--color-text-muted)] max-w-md mb-6 leading-relaxed">
        {description}
      </p>
      {action && <div>{action}</div>}
    </div>
  );
}
