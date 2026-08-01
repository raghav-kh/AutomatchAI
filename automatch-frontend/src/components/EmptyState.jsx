export default function EmptyState({ title, description, action }) {
  return (
    <div className="border border-dashed border-line rounded-lg p-10 text-center bg-surface">
      <div className="font-display font-semibold text-lg mb-1">{title}</div>
      <p className="text-ink-soft text-sm max-w-md mx-auto">{description}</p>
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}
