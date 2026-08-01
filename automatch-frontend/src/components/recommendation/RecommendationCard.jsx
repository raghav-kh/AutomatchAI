import { useState } from "react";
import { Link } from "react-router-dom";
import { Sparkles, ChevronDown, ChevronUp, ArrowRightLeft, Shield, Fuel, Zap, Award } from "lucide-react";
import ProgressRing from "../ui/ProgressRing";
import Badge from "../ui/Badge";
import Button from "../ui/Button";
import SolidCard from "../ui/SolidCard";
import LLMReasoningBox from "./LLMReasoningBox";
import FactorBreakdown from "./FactorBreakdown";

export default function RecommendationCard({ rec, rank = 0, onAddToCompare }) {
  const [expanded, setExpanded] = useState(false);
  const { variant, score, confidence, match_reasons, trade_offs, llm_explanation, score_breakdown } = rec;

  const formattedPrice = variant.price != null ? `₹${variant.price.toLocaleString("en-IN")}` : "Price N/A";
  const matchPercent = Math.round((score / 10) * 100);

  // Confidence styling
  let confidenceVariant = "neutral";
  if (confidence >= 80) confidenceVariant = "success";
  else if (confidence >= 50) confidenceVariant = "cyan";
  else confidenceVariant = "warning";

  return (
    <SolidCard className="border border-[var(--color-line-bright)] relative hover:border-indigo-500/40 transition-all">
      {/* Rank Indicator */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-4 border-b border-[var(--color-line)]">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-indigo-500 to-cyan-400 text-slate-950 font-display font-bold text-sm flex items-center justify-center shadow-sm">
            #{rank + 1}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold text-[var(--color-text-muted)] uppercase tracking-wider">
                {variant.manufacturer_name}
              </span>
              {rank === 0 && (
                <Badge variant="primary" icon={Award}>
                  Best Match
                </Badge>
              )}
            </div>
            <h3 className="text-xl font-bold font-display text-white">
              {variant.car_model} <span className="font-normal text-indigo-300 text-base">· {variant.variant_name}</span>
            </h3>
          </div>
        </div>

        {/* Score & Confidence */}
        <div className="flex items-center gap-4">
          <div className="text-right hidden sm:block">
            <div className="text-xs text-[var(--color-text-muted)]">Match Quality</div>
            <Badge variant={confidenceVariant} icon={Shield}>
              {confidence}% Confidence
            </Badge>
          </div>
          <ProgressRing
            value={score.toFixed(1)}
            max={10}
            size={58}
            strokeWidth={5}
            sublabel="Score"
            color={score >= 8 ? "var(--color-success)" : "var(--color-primary)"}
          />
        </div>
      </div>

      {/* Vehicle Specs Bar */}
      <div className="py-4 grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
        <div>
          <span className="text-[var(--color-text-dim)] uppercase tracking-wider block">Price (Ex-Showroom)</span>
          <span className="font-mono text-white text-sm font-semibold">{formattedPrice}</span>
        </div>
        <div>
          <span className="text-[var(--color-text-dim)] uppercase tracking-wider block">Fuel & Transmission</span>
          <span className="text-white font-medium">{variant.fuel || "—"} · {variant.transmission || "—"}</span>
        </div>
        <div>
          <span className="text-[var(--color-text-dim)] uppercase tracking-wider block">Safety Rating</span>
          <span className="text-emerald-400 font-medium">
            {variant.specifications?.safety_rating ? `${variant.specifications.safety_rating}/5 Star` : "Unrated"}
          </span>
        </div>
        <div>
          <span className="text-[var(--color-text-dim)] uppercase tracking-wider block">Mileage</span>
          <span className="font-mono text-cyan-400 font-medium">
            {variant.mileage ? `${variant.mileage} km/l` : "—"}
          </span>
        </div>
      </div>

      {/* LLM & Quick Tradeoffs Preview */}
      <div className="pt-2">
        <LLMReasoningBox
          explanation={llm_explanation}
          reasons={match_reasons}
          trade_offs={trade_offs}
        />
      </div>

      {/* Expandable Breakdown Drawer */}
      {expanded && (
        <div className="mt-4 pt-4 border-t border-[var(--color-line)] animate-fade-in">
          <FactorBreakdown breakdown={score_breakdown} />
        </div>
      )}

      {/* Card Footer Actions */}
      <div className="mt-4 pt-3 border-t border-[var(--color-line)] flex flex-wrap items-center justify-between gap-3">
        <button
          type="button"
          onClick={() => setExpanded(!expanded)}
          className="text-xs text-[var(--color-text-muted)] hover:text-white flex items-center gap-1 font-medium transition-colors"
        >
          {expanded ? (
            <>
              Hide 11-Factor Scores <ChevronUp className="w-4 h-4" />
            </>
          ) : (
            <>
              View 11-Factor Breakdown <ChevronDown className="w-4 h-4" />
            </>
          )}
        </button>

        <div className="flex items-center gap-2">
          {onAddToCompare && (
            <Button
              variant="secondary"
              size="sm"
              icon={ArrowRightLeft}
              onClick={() => onAddToCompare(variant)}
            >
              Compare
            </Button>
          )}
          <Link to={`/variants/${variant.id}`}>
            <Button variant="primary" size="sm">
              5-Year Ownership Cost & Details &rarr;
            </Button>
          </Link>
        </div>
      </div>
    </SolidCard>
  );
}
