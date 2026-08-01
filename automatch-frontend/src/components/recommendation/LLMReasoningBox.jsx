import { ShieldCheck, CheckCircle2, AlertTriangle, Cpu } from "lucide-react";
import Badge from "../ui/Badge";

export default function LLMReasoningBox({ explanation, reasons = [], trade_offs = [] }) {
  return (
    <div className="rounded-xl bg-slate-900/80 border border-indigo-500/20 p-4 space-y-3">
      <div className="flex items-center justify-between gap-2 border-b border-indigo-500/10 pb-2">
        <div className="flex items-center gap-2 text-xs font-semibold text-indigo-300">
          <Cpu className="w-4 h-4 text-cyan-400" />
          <span>AI Decision Rationale</span>
        </div>
        <Badge variant="success" icon={ShieldCheck}>
          Consistency Guard Verified
        </Badge>
      </div>

      {explanation && (
        <p className="text-xs text-[var(--color-text-muted)] italic leading-relaxed pl-3 border-l-2 border-cyan-500/40">
          "{explanation}"
        </p>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
        {reasons.length > 0 && (
          <div className="space-y-1.5">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-emerald-400 flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5" /> Key Strengths
            </span>
            <ul className="space-y-1">
              {reasons.map((r, i) => (
                <li key={i} className="text-xs text-emerald-200/90 flex items-start gap-1.5">
                  <span className="text-emerald-400">•</span>
                  <span>{r}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {trade_offs.length > 0 && (
          <div className="space-y-1.5">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-amber-400 flex items-center gap-1">
              <AlertTriangle className="w-3.5 h-3.5" /> Key Trade-offs
            </span>
            <ul className="space-y-1">
              {trade_offs.map((t, i) => (
                <li key={i} className="text-xs text-amber-200/90 flex items-start gap-1.5">
                  <span className="text-amber-400">•</span>
                  <span>{t}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
