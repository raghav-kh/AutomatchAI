import { Link } from "react-router-dom";
import ConfidenceGauge from "./ConfidenceGauge";
import ScoreBar from "./ScoreBar";

const RANK_LABEL = ["1st pick", "2nd pick", "3rd pick"];

export default function RecommendationCard({ rec, rank }) {
  const { variant, car, manufacturer_name, score_breakdown, confidence, reasons, trade_offs, explanation } = rec;
  const components = Object.entries(score_breakdown).filter(([key]) => key !== "total");

  return (
    <article className="bg-surface border border-line rounded-lg p-5">
      <div className="flex items-start justify-between gap-4">
        <div>
          {rank !== undefined && rank < 3 && (
            <div className="text-[11px] uppercase tracking-wide text-accent font-semibold mb-1">
              {RANK_LABEL[rank]}
            </div>
          )}
          <h3 className="font-display font-semibold text-xl">
            {manufacturer_name} {car.model}
          </h3>
          <div className="text-ink-soft text-sm">{variant.variant_name}</div>
          <div className="font-data text-lg mt-1">
            {variant.price != null ? `₹${variant.price.toLocaleString("en-IN")}` : "Price unavailable"}
          </div>
        </div>
        <ConfidenceGauge value={confidence} />
      </div>

      <p className="mt-4 text-sm leading-relaxed">{explanation}</p>

      <div className="mt-4 grid sm:grid-cols-2 gap-x-6 gap-y-1.5">
        {components.map(([key, value]) => (
          <ScoreBar key={key} componentKey={key} value={value} />
        ))}
      </div>

      <div className="mt-4 flex flex-wrap gap-2">
        {reasons.map((r) => (
          <span key={r} className="text-xs bg-accent-soft text-accent px-2 py-1 rounded-full">
            {r}
          </span>
        ))}
        {trade_offs.map((t) => (
          <span key={t} className="text-xs bg-caution-soft text-caution px-2 py-1 rounded-full">
            {t}
          </span>
        ))}
      </div>

      <div className="mt-4 pt-4 border-t border-line flex gap-4 text-sm">
        <Link to={`/variants/${variant.id}`} className="text-primary font-medium hover:underline">
          Ownership cost &amp; alternatives &rarr;
        </Link>
      </div>
    </article>
  );
}
