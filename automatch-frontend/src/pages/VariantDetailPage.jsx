import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getVariant, getOwnershipCost, getAlternatives } from "../api/client";
import EmptyState from "../components/EmptyState";

function money(v) {
  return v != null ? `₹${Math.round(v).toLocaleString("en-IN")}` : "—";
}

const COST_ROWS = [
  ["purchase_price", "Purchase price"],
  ["insurance_total", "Insurance (total)"],
  ["fuel_total", "Fuel (total)"],
  ["maintenance_total", "Maintenance (total)"],
  ["road_tax", "Road tax"],
];

export default function VariantDetailPage() {
  const { id } = useParams();
  const [variant, setVariant] = useState(null);
  const [cost, setCost] = useState(null);
  const [alternatives, setAlternatives] = useState(null);
  const [annualKm, setAnnualKm] = useState(12000);
  const [years, setYears] = useState(5);
  const [error, setError] = useState("");

  useEffect(() => {
    getVariant(id)
      .then(setVariant)
      .catch(() => setError("Couldn't load this variant."));
    getAlternatives(id).then(setAlternatives).catch(() => setAlternatives([]));
  }, [id]);

  useEffect(() => {
    getOwnershipCost(id, { annual_km: annualKm, ownership_years: years })
      .then(setCost)
      .catch(() => setError("Couldn't calculate ownership cost."));
  }, [id, annualKm, years]);

  if (error) {
    return <EmptyState title="Something went wrong" description={error} />;
  }
  if (!variant) {
    return <div className="text-ink-soft text-sm">Loading…</div>;
  }

  return (
    <div>
      <Link to="/" className="text-sm text-primary hover:underline">
        &larr; Back
      </Link>

      <header className="mt-3 mb-6">
        <h1 className="font-display font-semibold text-2xl">{variant.variant_name}</h1>
        <div className="font-data text-lg mt-1">{money(variant.price)}</div>
      </header>

      <section className="bg-surface border border-line rounded-lg p-5 mb-6">
        <h2 className="font-display font-semibold text-lg mb-3">Ownership cost (SRS 4.5)</h2>

        <div className="flex flex-wrap gap-4 mb-4">
          <label className="flex flex-col gap-1 text-sm">
            <span className="font-medium">Annual driving (km)</span>
            <input
              type="number"
              className="border border-line rounded-md px-3 py-2 w-32"
              value={annualKm}
              onChange={(e) => setAnnualKm(Number(e.target.value))}
            />
          </label>
          <label className="flex flex-col gap-1 text-sm">
            <span className="font-medium">Ownership years</span>
            <input
              type="number"
              min={1}
              max={15}
              className="border border-line rounded-md px-3 py-2 w-24"
              value={years}
              onChange={(e) => setYears(Number(e.target.value))}
            />
          </label>
        </div>

        {cost && (
          <>
            <dl className="grid sm:grid-cols-2 gap-x-8 gap-y-2 text-sm">
              {COST_ROWS.map(([key, label]) => (
                <div key={key} className="flex justify-between border-b border-line py-1.5">
                  <dt className="text-ink-soft">{label}</dt>
                  <dd className="font-data">{money(cost[key])}</dd>
                </div>
              ))}
              <div className="flex justify-between border-b border-line py-1.5">
                <dt className="text-ink-soft">Expected resale value</dt>
                <dd className="font-data text-accent">{money(cost.expected_resale_value)}</dd>
              </div>
            </dl>

            <div className="mt-4 pt-4 border-t-2 border-ink flex justify-between items-baseline">
              <span className="font-medium">
                Net {years}-year cost of ownership
              </span>
              <span className="font-data text-2xl font-semibold">{money(cost.net_cost_after_resale)}</span>
            </div>

            <p className="text-xs text-ink-soft mt-3">{cost.assumptions?.note}</p>
          </>
        )}
      </section>

      <section className="bg-surface border border-line rounded-lg p-5">
        <h2 className="font-display font-semibold text-lg mb-3">You may also consider (SRS 4.7)</h2>

        {alternatives === null && <p className="text-sm text-ink-soft">Loading…</p>}
        {alternatives && alternatives.length === 0 && (
          <p className="text-sm text-ink-soft">No clearly better alternatives found in a similar price range.</p>
        )}
        {alternatives && alternatives.length > 0 && (
          <div className="grid gap-3">
            {alternatives.map((alt) => (
              <div key={alt.variant_id} className="border border-line rounded-md p-3">
                <div className="flex justify-between items-baseline">
                  <Link to={`/variants/${alt.variant_id}`} className="font-medium hover:underline">
                    {alt.manufacturer_name} {alt.car_model} — {alt.variant_name}
                  </Link>
                  <span className="font-data text-sm text-ink-soft">
                    {alt.price_difference >= 0 ? "+" : ""}
                    {money(alt.price_difference)}
                  </span>
                </div>
                <div className="flex flex-wrap gap-2 mt-2">
                  {alt.reasons.map((r) => (
                    <span key={r} className="text-xs bg-accent-soft text-accent px-2 py-1 rounded-full">
                      {r}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
