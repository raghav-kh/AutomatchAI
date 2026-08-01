import { AlertTriangle, RefreshCw } from "lucide-react";
import Button from "./Button";

export default function ErrorAlert({
  title = "Something went wrong",
  message = "Unable to complete request. Please verify your server connection and try again.",
  onRetry = null,
  className = "",
}) {
  return (
    <div className={`rounded-xl p-4 bg-[var(--color-danger-soft)] border border-[var(--color-danger)]/30 text-red-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 ${className}`} role="alert">
      <div className="flex items-start gap-3">
        <AlertTriangle className="w-5 h-5 text-[var(--color-danger)] shrink-0 mt-0.5" aria-hidden="true" />
        <div>
          <h4 className="text-sm font-semibold text-white">{title}</h4>
          <p className="text-xs text-red-300/90 mt-0.5 leading-relaxed">{message}</p>
        </div>
      </div>
      {onRetry && (
        <Button variant="danger" size="sm" onClick={onRetry} icon={RefreshCw} className="shrink-0">
          Retry
        </Button>
      )}
    </div>
  );
}
