import SectionHeading from "../components/ui/SectionHeading";
import SolidCard from "../components/ui/SolidCard";
import Badge from "../components/ui/Badge";
import { Sliders, ShieldCheck, Cpu } from "lucide-react";

export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-8 md:py-12 space-y-8 animate-fade-in">
      <SectionHeading
        badge={<Badge variant="cyan" icon={Cpu}>Engine Architecture</Badge>}
        title="About AutoMatch AI"
        subtitle="Built to solve the fundamental flaw in conventional car shopping platforms."
      />

      <SolidCard className="border border-[var(--color-line-bright)] space-y-4">
        <h3 className="text-xl font-bold font-display text-white">The Core Problem</h3>
        <p className="text-sm text-[var(--color-text-muted)] leading-relaxed">
          Most car-shopping portals assume buyers already know which specific models to compare. When a user filters by price, platforms surface only the most common brand names, causing buyers to miss excellent vehicles they simply didn't know existed.
        </p>
        <p className="text-sm text-[var(--color-text-muted)] leading-relaxed">
          AutoMatch AI works backwards from what buyers actually know — their budget, family seating needs, daily commute distance, and road usage — dynamically evaluating vehicles across 11 weighted scoring parameters.
        </p>
      </SolidCard>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <SolidCard className="space-y-2 border border-[var(--color-line)]">
          <div className="flex items-center gap-2 text-indigo-400 font-bold font-display">
            <Sliders className="w-5 h-5" /> 11-Factor Weighted Engine
          </div>
          <p className="text-xs text-[var(--color-text-muted)] leading-relaxed">
            Weights shift dynamically based on user priorities (e.g. high safety rating requirement increases GNCAP weight; long daily commute shifts EV vs Petrol fuel scores).
          </p>
        </SolidCard>

        <SolidCard className="space-y-2 border border-[var(--color-line)]">
          <div className="flex items-center gap-2 text-cyan-400 font-bold font-display">
            <ShieldCheck className="w-5 h-5" /> AI Consistency Guard
          </div>
          <p className="text-xs text-[var(--color-text-muted)] leading-relaxed">
            LLM explanations are generated via Groq (Llama 3.3) and validated against a consistency guard that rejects any response contradicting the mathematical score.
          </p>
        </SolidCard>
      </div>
    </div>
  );
}
