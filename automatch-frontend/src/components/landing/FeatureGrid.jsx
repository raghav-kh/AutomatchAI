import SectionHeading from "../ui/SectionHeading";
import SolidCard from "../ui/SolidCard";
import Badge from "../ui/Badge";
import { Sliders, Cpu, Calculator, Scale, Sparkles, Database } from "lucide-react";

const FEATURES = [
  {
    icon: Sliders,
    color: "text-indigo-400",
    title: "11-Factor Weighted Engine",
    description: "Evaluates budget fit, safety ratings, family seating, commute cost, maintenance, resale value, and parking dimensions with dynamic weight shifting.",
  },
  {
    icon: Cpu,
    color: "text-cyan-400",
    title: "Explainable AI & Guard",
    description: "LLM explanations generated via Groq (Llama 3.3) paired with an automated consistency guard that rejects any contradiction against real scores.",
  },
  {
    icon: Calculator,
    color: "text-emerald-400",
    title: "5-Year Ownership Cost",
    description: "Models purchase price, insurance, fuel/energy expenses, maintenance schedules, road tax, and expected resale value with clear assumptions.",
  },
  {
    icon: Scale,
    color: "text-amber-400",
    title: "Multi-Car Comparison",
    description: "Side-by-side technical matrix highlighting winning specs, airbags, boot capacity, power outputs, and overall recommendation scores.",
  },
  {
    icon: Sparkles,
    color: "text-purple-400",
    title: "Alternative Recommendations",
    description: "'You may also consider X because...' algorithm surfaces hidden gems with explicit price delta callouts and rationale tags.",
  },
  {
    icon: Database,
    color: "text-blue-400",
    title: "Live Data Ingestion",
    description: "Automated Web scrapers against official pricing portals and direct REST API ingestion with confidence scoring and audit logging.",
  },
];

export default function FeatureGrid() {
  return (
    <section className="py-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <SectionHeading
        align="center"
        badge={<Badge variant="cyan">System Architecture</Badge>}
        title="Engineered Against a 13-Section SRS Specification"
        subtitle="Built from the ground up to solve complex car decision problems for Indian buyers."
      />

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {FEATURES.map((f, idx) => {
          const Icon = f.icon;
          return (
            <SolidCard key={idx} hover className="border border-[var(--color-line-bright)] space-y-3">
              <div className="w-10 h-10 rounded-xl bg-[var(--color-surface-subtle)] flex items-center justify-center border border-[var(--color-line)]">
                <Icon className={`w-5 h-5 ${f.color}`} />
              </div>
              <h3 className="text-lg font-bold font-display text-white">{f.title}</h3>
              <p className="text-xs text-[var(--color-text-muted)] leading-relaxed">{f.description}</p>
            </SolidCard>
          );
        })}
      </div>
    </section>
  );
}
