import { ShieldCheck, Database, Sliders, RefreshCw } from "lucide-react";

const METRICS = [
  { icon: Database, label: "Dataset Coverage", value: "7+ Brands · 13+ Variants", sub: "India Market Focus" },
  { icon: ShieldCheck, label: "Confidence Scoring", value: "Multi-Source Trust", sub: "Data Integrity Rating" },
  { icon: Sliders, label: "Recommendation Logic", value: "11 Weighted Factors", sub: "Zero Brand Bias" },
  { icon: RefreshCw, label: "Data Freshness", value: "Automated Ingestion", sub: "Audited Ingestion Logs" },
];

export default function DatasetMetricsBar() {
  return (
    <section className="py-10 border-y border-[var(--color-line)] bg-slate-950/60">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 text-center">
          {METRICS.map((m, idx) => {
            const Icon = m.icon;
            return (
              <div key={idx} className="space-y-1.5 p-4 rounded-xl bg-white/[0.02] border border-[var(--color-line)]">
                <Icon className="w-5 h-5 text-cyan-400 mx-auto mb-2" />
                <div className="font-mono text-base font-bold text-white">{m.value}</div>
                <div className="text-xs font-semibold text-[var(--color-text-main)]">{m.label}</div>
                <div className="text-[10px] text-[var(--color-text-dim)] uppercase tracking-wider">{m.sub}</div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
