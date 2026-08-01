import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getVariant, getOwnershipCost, getAlternatives } from "../api/client";
import SectionHeading from "../components/ui/SectionHeading";
import SolidCard from "../components/ui/SolidCard";
import Badge from "../components/ui/Badge";
import Button from "../components/ui/Button";
import EmptyState from "../components/ui/EmptyState";
import ErrorAlert from "../components/ui/ErrorAlert";
import { CardSkeleton } from "../components/ui/Skeleton";
import { ArrowLeft, Calculator, Sparkles, Shield, Fuel, DollarSign, ExternalLink } from "lucide-react";

function money(v) {
  return v != null ? `₹${Math.round(v).toLocaleString("en-IN")}` : "—";
}

const COST_ROWS = [
  ["purchase_price", "Purchase Price (ex-showroom)"],
  ["insurance_total", "Insurance (5-Year Total)"],
  ["fuel_total", "Estimated Fuel / Energy Cost"],
  ["maintenance_total", "Scheduled Maintenance & Service"],
  ["road_tax", "Road Tax & Registration"],
];

export default function VariantDetailPage() {
  const { id } = useParams();
  const [variant, setVariant] = useState(null);
  const [cost, setCost] = useState(null);
  const [alternatives, setAlternatives] = useState(null);
  const [annualKm, setAnnualKm] = useState(12000);
  const [years, setYears] = useState(5);
  const [status, setStatus] = useState("loading");
  const [error, setError] = useState("");

  useEffect(() => {
    setStatus("loading");
    getVariant(id)
      .then((data) => {
        setVariant(data);
        setStatus("idle");
      })
      .catch(() => {
        setStatus("error");
        setError("Unable to retrieve vehicle variant details.");
      });

    getAlternatives(id)
      .then(setAlternatives)
      .catch(() => setAlternatives([]));
  }, [id]);

  useEffect(() => {
    if (id) {
      getOwnershipCost(id, { annual_km: annualKm, ownership_years: years })
        .then(setCost)
        .catch(() => {});
    }
  }, [id, annualKm, years]);

  if (status === "loading") {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">
        <CardSkeleton />
        <CardSkeleton />
      </div>
    );
  }

  if (status === "error" || !variant) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-12">
        <ErrorAlert title="Variant Not Found" message={error} />
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 md:py-12 space-y-8 animate-fade-in">
      <Link to="/recommend" className="inline-flex items-center gap-1.5 text-xs text-indigo-400 hover:text-white font-medium transition-colors">
        <ArrowLeft className="w-4 h-4" /> Back to Recommendations
      </Link>

      {/* Hero Header Card */}
      <SolidCard className="border border-[var(--color-line-bright)] relative overflow-hidden">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-[var(--color-line)]">
          <div>
            <span className="text-xs font-semibold text-cyan-400 uppercase tracking-wider">
              {variant.manufacturer_name}
            </span>
            <h1 className="text-2xl md:text-3xl font-bold font-display text-white">
              {variant.car_model} <span className="font-normal text-indigo-300">· {variant.variant_name}</span>
            </h1>
          </div>
          <div className="text-right">
            <span className="text-xs text-[var(--color-text-dim)] uppercase tracking-wider block">Ex-Showroom Price</span>
            <span className="font-mono text-2xl font-bold text-white">{money(variant.price)}</span>
          </div>
        </div>

        <div className="pt-4 flex flex-wrap gap-2">
          {variant.fuel && <Badge variant="primary">{variant.fuel}</Badge>}
          {variant.transmission && <Badge variant="cyan">{variant.transmission}</Badge>}
          {variant.specifications?.safety_rating && (
            <Badge variant="success" icon={Shield}>
              {variant.specifications.safety_rating}/5 Safety Rating
            </Badge>
          )}
          {variant.mileage && <Badge variant="neutral">{variant.mileage} km/l</Badge>}
        </div>
      </SolidCard>

      {/* 5-Year Ownership Cost Calculator (SRS Section 4.5) */}
      <SolidCard className="border border-[var(--color-line-bright)] space-y-6">
        <div className="flex items-center justify-between border-b border-[var(--color-line)] pb-3">
          <div className="flex items-center gap-2">
            <Calculator className="w-5 h-5 text-indigo-400" />
            <h2 className="text-lg font-bold font-display text-white">
              5-Year Ownership Cost Estimator (SRS §4.5)
            </h2>
          </div>
          <Badge variant="cyan">Transparent Breakdown</Badge>
        </div>

        {/* Dynamic Controls */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-[var(--color-surface-subtle)] p-4 rounded-xl border border-[var(--color-line)]">
          <label className="flex flex-col gap-1.5 text-xs">
            <span className="font-medium text-[var(--color-text-muted)]">Annual Driving Distance (km/year)</span>
            <input
              type="number"
              min={1000}
              step={1000}
              value={annualKm}
              onChange={(e) => setAnnualKm(Number(e.target.value))}
              className="bg-[var(--color-surface-solid)] border border-[var(--color-line)] rounded-lg px-3 py-2 font-mono text-white"
            />
          </label>
          <label className="flex flex-col gap-1.5 text-xs">
            <span className="font-medium text-[var(--color-text-muted)]">Ownership Duration (Years)</span>
            <input
              type="number"
              min={1}
              max={15}
              value={years}
              onChange={(e) => setYears(Number(e.target.value))}
              className="bg-[var(--color-surface-solid)] border border-[var(--color-line)] rounded-lg px-3 py-2 font-mono text-white"
            />
          </label>
        </div>

        {cost && (
          <div className="space-y-4">
            <dl className="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-3 text-sm">
              {COST_ROWS.map(([key, label]) => (
                <div key={key} className="flex justify-between items-center border-b border-[var(--color-line)] pb-2">
                  <dt className="text-[var(--color-text-muted)] text-xs">{label}</dt>
                  <dd className="font-mono text-white font-medium">{money(cost[key])}</dd>
                </div>
              ))}
              <div className="flex justify-between items-center border-b border-[var(--color-line)] pb-2">
                <dt className="text-[var(--color-text-muted)] text-xs">Expected Resale Value after {years} Years</dt>
                <dd className="font-mono text-emerald-400 font-medium">-{money(cost.expected_resale_value)}</dd>
              </div>
            </dl>

            <div className="pt-4 border-t-2 border-indigo-500/50 flex items-baseline justify-between bg-indigo-500/10 p-4 rounded-xl border border-indigo-500/30">
              <div>
                <div className="font-display font-bold text-lg text-white">Net {years}-Year Total Cost</div>
                <div className="text-xs text-[var(--color-text-muted)]">Includes depreciation & resale recovery</div>
              </div>
              <div className="font-mono text-3xl font-bold text-cyan-400">
                {money(cost.net_cost_after_resale)}
              </div>
            </div>

            {cost.assumptions?.note && (
              <p className="text-xs text-[var(--color-text-dim)] italic">
                Note: {cost.assumptions.note}
              </p>
            )}
          </div>
        )}
      </SolidCard>

      {/* "You May Also Consider" Alternatives (SRS Section 4.7) */}
      <SolidCard className="border border-[var(--color-line-bright)] space-y-4">
        <div className="flex items-center gap-2 border-b border-[var(--color-line)] pb-3">
          <Sparkles className="w-5 h-5 text-cyan-400" />
          <h2 className="text-lg font-bold font-display text-white">
            You May Also Consider (SRS §4.7)
          </h2>
        </div>

        {alternatives === null && <div className="text-xs text-[var(--color-text-muted)]">Loading alternative models…</div>}
        {alternatives && alternatives.length === 0 && (
          <p className="text-xs text-[var(--color-text-muted)]">No better alternatives found within a similar budget bracket.</p>
        )}

        {alternatives && alternatives.length > 0 && (
          <div className="grid gap-3">
            {alternatives.map((alt) => (
              <div key={alt.variant_id} className="p-4 rounded-xl bg-[var(--color-surface-subtle)] border border-[var(--color-line)] flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div>
                  <Link to={`/variants/${alt.variant_id}`} className="font-bold text-white hover:text-cyan-400 transition-colors flex items-center gap-1.5">
                    {alt.manufacturer_name} {alt.car_model} — {alt.variant_name}
                    <ExternalLink className="w-3.5 h-3.5" />
                  </Link>
                  <div className="flex flex-wrap gap-1.5 mt-2">
                    {alt.reasons.map((r, idx) => (
                      <Badge key={idx} variant="cyan">{r}</Badge>
                    ))}
                  </div>
                </div>
                <div className="font-mono text-sm font-semibold text-right">
                  <span className={alt.price_difference >= 0 ? "text-amber-400" : "text-emerald-400"}>
                    {alt.price_difference >= 0 ? "+" : ""}
                    {money(alt.price_difference)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </SolidCard>
    </div>
  );
}
