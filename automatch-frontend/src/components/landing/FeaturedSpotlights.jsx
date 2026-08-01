import { Link } from "react-router-dom";
import spotlightsData from "../../data/featuredSpotlights.json";
import SectionHeading from "../ui/SectionHeading";
import SolidCard from "../ui/SolidCard";
import Badge from "../ui/Badge";
import { CheckCircle2, ArrowRight } from "lucide-react";

export default function FeaturedSpotlights() {
  return (
    <section className="py-12 bg-slate-950/40 border-y border-[var(--color-line)]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <SectionHeading
          align="center"
          badge={<Badge variant="primary">Real Worked Examples</Badge>}
          title="See How AutoMatch AI Solves Real Buyer Dilemmas"
          subtitle="A ₹10L SUV budget shouldn't surface Tata Nexon alone — it should surface the Citroën Basalt too."
        />

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {spotlightsData.map((item) => (
            <SolidCard key={item.id} hover className="border border-[var(--color-line-bright)] flex flex-col justify-between space-y-4">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <Badge variant="cyan">{item.badge}</Badge>
                  <span className="text-[10px] font-mono text-[var(--color-text-dim)]">{item.budget}</span>
                </div>

                <h3 className="text-xl font-bold font-display text-white">{item.title}</h3>
                <p className="text-xs text-[var(--color-text-muted)] leading-relaxed">{item.subtitle}</p>

                <div className="p-3 rounded-xl bg-[var(--color-surface-subtle)] border border-[var(--color-line)] space-y-1">
                  <span className="text-[10px] font-mono text-emerald-400 uppercase tracking-wider block">Top Recommendation Winner</span>
                  <div className="text-xs font-bold text-white">{item.winner}</div>
                </div>

                <div className="space-y-1.5 pt-1">
                  <span className="text-[11px] font-semibold text-[var(--color-text-muted)] uppercase tracking-wider block">Key Decision Factors</span>
                  {item.reasons.map((r, i) => (
                    <div key={i} className="text-xs text-[var(--color-text-muted)] flex items-start gap-1.5">
                      <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400 shrink-0 mt-0.5" />
                      <span>{r}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="pt-2">
                <Link to="/recommend" className="text-xs text-indigo-400 hover:text-white font-semibold flex items-center gap-1 transition-colors">
                  Try This Recommendation Scenario <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </SolidCard>
          ))}
        </div>
      </div>
    </section>
  );
}
