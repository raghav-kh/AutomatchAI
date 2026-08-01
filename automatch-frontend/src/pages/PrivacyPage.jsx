import SectionHeading from "../components/ui/SectionHeading";
import SolidCard from "../components/ui/SolidCard";
import Badge from "../components/ui/Badge";
import { Shield } from "lucide-react";

export default function PrivacyPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-8 md:py-12 space-y-8 animate-fade-in">
      <SectionHeading
        badge={<Badge variant="success" icon={Shield}>Zero Tracking</Badge>}
        title="Privacy & Data Neutrality Policy"
        subtitle="AutoMatch AI prioritizes user privacy and uncompromised recommendation neutrality."
      />

      <SolidCard className="border border-[var(--color-line-bright)] space-y-4">
        <h3 className="text-xl font-bold font-display text-white">1. No Personal Data Storage</h3>
        <p className="text-sm text-[var(--color-text-muted)] leading-relaxed">
          The recommendation engine processes your budget and driving preferences purely in-memory to generate rank scores. We do not track, store, or sell your personal search history or contact details to third-party dealerships.
        </p>

        <h3 className="text-xl font-bold font-display text-white pt-2">2. Unbiased Manufacturer Scoring</h3>
        <p className="text-sm text-[var(--color-text-muted)] leading-relaxed">
          Recommendations are computed strictly using open technical specs, GNCAP safety scores, and verified user cost models. No manufacturer or dealer can pay for sponsored positioning or score boosts.
        </p>
      </SolidCard>
    </div>
  );
}
