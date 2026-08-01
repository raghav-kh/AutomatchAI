export default function Skeleton({ className = "", height, width }) {
  const style = {};
  if (height) style.height = height;
  if (width) style.width = width;

  return (
    <div
      style={style}
      className={`animate-pulse bg-[var(--color-surface-subtle)] rounded-lg ${className}`}
      aria-hidden="true"
    />
  );
}

export function CardSkeleton() {
  return (
    <div className="solid-card rounded-xl p-5 space-y-4">
      <div className="flex justify-between items-center">
        <Skeleton className="h-6 w-1/3" />
        <Skeleton className="h-10 w-10 rounded-full" />
      </div>
      <Skeleton className="h-4 w-1/2" />
      <div className="space-y-2 pt-2">
        <Skeleton className="h-3 w-full" />
        <Skeleton className="h-3 w-4/5" />
      </div>
      <div className="flex gap-2 pt-3">
        <Skeleton className="h-8 w-24 rounded-full" />
        <Skeleton className="h-8 w-24 rounded-full" />
      </div>
    </div>
  );
}

export function TableRowSkeleton({ columns = 4 }) {
  return (
    <tr className="border-b border-[var(--color-line)] animate-pulse">
      {Array.from({ length: columns }).map((_, i) => (
        <td key={i} className="p-4">
          <Skeleton className="h-4 w-full" />
        </td>
      ))}
    </tr>
  );
}
