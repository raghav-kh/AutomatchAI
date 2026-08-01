import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Sparkles, ArrowRight, Car, ShieldCheck, CheckCircle } from "lucide-react";
import Button from "../ui/Button";
import GlassCard from "../ui/GlassCard";
import Badge from "../ui/Badge";

export default function HeroSection() {
  const navigate = useNavigate();

  // High-converting quick match widget state
  const [budgetLakh, setBudgetLakh] = useState("10");
  const [familyMembers, setFamilyMembers] = useState("4");
  const [bodyType, setBodyType] = useState("SUV");

  function handleQuickMatch(e) {
    e.preventDefault();
    const budgetNum = Number(budgetLakh) * 100000;
    navigate(`/recommend?budget=${budgetNum}&family=${familyMembers}&body=${bodyType}`);
  }

  return (
    <div className="relative overflow-hidden py-12 md:py-20 lg:py-24">
      {/* Glow Effects Background */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[350px] bg-indigo-600/15 rounded-full blur-[140px] pointer-events-none" />
      <div className="absolute top-1/3 right-10 w-[400px] h-[250px] bg-cyan-500/10 rounded-full blur-[120px] pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          
          {/* Left Column: Hero Copy */}
          <div className="lg:col-span-7 space-y-6 text-center lg:text-left">
            <Badge variant="cyan" icon={Sparkles} className="mx-auto lg:mx-0">
              AI Decision System for Indian Car Buyers
            </Badge>

            <h1 className="text-3xl sm:text-5xl lg:text-6xl font-bold font-display tracking-tight text-white leading-[1.1]">
              Stop Filtering Specs. <br />
              <span className="bg-gradient-to-r from-indigo-400 via-cyan-300 to-emerald-400 bg-clip-text text-transparent">
                Start Matching Your Life.
              </span>
            </h1>

            <p className="text-base sm:text-lg text-[var(--color-text-muted)] max-w-2xl mx-auto lg:mx-0 leading-relaxed">
              AutoMatch AI works backwards from what buyers actually know — budget, family size, commute, and road habits — surfacing the right cars, including ones you'd never think to search for.
            </p>

            <div className="pt-2 flex flex-wrap items-center justify-center lg:justify-start gap-4">
              <Button
                variant="cyan"
                size="lg"
                icon={Sparkles}
                onClick={() => navigate("/recommend")}
              >
                Launch AI Car Matcher
              </Button>
              <Button
                variant="secondary"
                size="lg"
                icon={ArrowRight}
                onClick={() => navigate("/compare")}
              >
                Smart Compare
              </Button>
            </div>

            {/* Feature Bullets */}
            <div className="pt-4 flex flex-wrap items-center justify-center lg:justify-start gap-6 text-xs text-[var(--color-text-muted)]">
              <span className="flex items-center gap-1.5"><CheckCircle className="w-4 h-4 text-emerald-400" /> 11 Weighted Factors</span>
              <span className="flex items-center gap-1.5"><CheckCircle className="w-4 h-4 text-cyan-400" /> Groq AI Explanations</span>
              <span className="flex items-center gap-1.5"><CheckCircle className="w-4 h-4 text-indigo-400" /> 5-Yr Ownership Cost</span>
            </div>
          </div>

          {/* Right Column: High-Converting Quick Match Teaser Widget */}
          <div className="lg:col-span-5">
            <GlassCard glow className="border border-[var(--color-line-bright)] space-y-5">
              <div className="flex items-center justify-between border-b border-[var(--color-line)] pb-3">
                <div className="flex items-center gap-2">
                  <Car className="w-5 h-5 text-cyan-400" />
                  <h3 className="font-display font-bold text-base text-white">Quick Match Teaser</h3>
                </div>
                <Badge variant="success">Instant AI</Badge>
              </div>

              <form onSubmit={handleQuickMatch} className="space-y-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-semibold text-[var(--color-text-muted)] flex justify-between">
                    <span>What's your budget?</span>
                    <span className="font-mono text-cyan-400 font-bold">₹{budgetLakh} Lakh</span>
                  </label>
                  <input
                    type="range"
                    min={5}
                    max={40}
                    step={1}
                    value={budgetLakh}
                    onChange={(e) => setBudgetLakh(e.target.value)}
                    className="w-full accent-[var(--color-accent-cyan)] cursor-pointer"
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <label className="flex flex-col gap-1.5 text-xs">
                    <span className="font-semibold text-[var(--color-text-muted)]">Family Size</span>
                    <select
                      value={familyMembers}
                      onChange={(e) => setFamilyMembers(e.target.value)}
                      className="bg-[var(--color-surface-subtle)] border border-[var(--color-line)] rounded-xl px-3 py-2 text-white font-medium focus:border-[var(--color-primary)]"
                    >
                      <option value="2">2 Members</option>
                      <option value="4">4 Members</option>
                      <option value="5">5 Members</option>
                      <option value="7">7 Members</option>
                    </select>
                  </label>

                  <label className="flex flex-col gap-1.5 text-xs">
                    <span className="font-semibold text-[var(--color-text-muted)]">Body Style</span>
                    <select
                      value={bodyType}
                      onChange={(e) => setBodyType(e.target.value)}
                      className="bg-[var(--color-surface-subtle)] border border-[var(--color-line)] rounded-xl px-3 py-2 text-white font-medium focus:border-[var(--color-primary)]"
                    >
                      <option value="Hatchback">Hatchback</option>
                      <option value="Sedan">Sedan</option>
                      <option value="SUV">SUV</option>
                      <option value="MPV">MPV</option>
                    </select>
                  </label>
                </div>

                <Button type="submit" variant="primary" size="lg" icon={Sparkles} className="w-full mt-2">
                  Find My Match &rarr;
                </Button>
              </form>
            </GlassCard>
          </div>

        </div>
      </div>
    </div>
  );
}
