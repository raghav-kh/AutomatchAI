import { useNavigate } from "react-router-dom";
import { Sparkles, ArrowRightLeft } from "lucide-react";
import Button from "../ui/Button";
import GlassCard from "../ui/GlassCard";

export default function LandingCTA() {
  const navigate = useNavigate();

  return (
    <section className="py-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <GlassCard glow className="border border-[var(--color-line-bright)] text-center py-12 px-6 sm:px-12 space-y-6">
        <h2 className="text-2xl sm:text-4xl font-bold font-display text-white max-w-2xl mx-auto leading-tight">
          Ready to Discover Your Ideal Car in 2 Minutes?
        </h2>
        <p className="text-sm sm:text-base text-[var(--color-text-muted)] max-w-xl mx-auto leading-relaxed">
          No sign-up required for buyers. State your budget, family size, and driving preferences to get plain-language recommendations instantly.
        </p>
        <div className="flex flex-wrap justify-center gap-4 pt-2">
          <Button variant="cyan" size="lg" icon={Sparkles} onClick={() => navigate("/recommend")}>
            Launch AI Matcher
          </Button>
          <Button variant="secondary" size="lg" icon={ArrowRightLeft} onClick={() => navigate("/compare")}>
            Compare Car Models
          </Button>
        </div>
      </GlassCard>
    </section>
  );
}
