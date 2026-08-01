import { useEffect, useState } from "react";
import { listCars, listVariantsForCar, compareVariants } from "../api/client";
import EmptyState from "../components/EmptyState";
import { Link } from "react-router-dom";

const ROWS = [
  { key: "price", label: "Price", fmt: (v) => (v != null ? `₹${v.toLocaleString("en-IN")}` : "—") },
  { key: "power", label: "Power", fmt: (v) => v ?? "—" },
  { key: "torque", label: "Torque", fmt: (v) => v ?? "—" },
  { key: "mileage", label: "Mileage", fmt: (v) => (v != null ? `${v} km/l` : "—") },
  { key: "safety_rating", label: "Safety rating", fmt: (v) => (v != null ? `${v}/5` : "—") },
  { key: "airbags", label: "Airbags", fmt: (v) => v ?? "—" },
  { key: "maintenance_level", label: "Maintenance level", fmt: (v) => (v != null ? `${v}/10` : "—") },
  { key: "boot_space", label: "Boot space", fmt: (v) => (v != null ? `${v} L` : "—") },
  { key: "ground_clearance", label: "Ground clearance", fmt: (v) => (v != null ? `${v} mm` : "—") },
  { key: "family_score", label: "Family fit score", fmt: (v) => (v != null ? `${v}/10` : "—") },
  { key: "ai_recommendation_score", label: "AI recommendation score", fmt: (v) => `${v.toFixed(1)}/10` },
];

export default function ComparePage() {
  const [cars, setCars] = useState([]);
  const [selectedCarId, setSelectedCarId] = useState("");
  const [carVariants, setCarVariants] = useState([]);
  const [selectedVariantId, setSelectedVariantId] = useState("");
  const [picked, setPicked] = useState([]); // [{variant_id, car_model, variant_name}]
  const [rows, setRows] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    listCars({ limit: 500 }).then(setCars).catch(() => setError("Couldn't load cars from the API."));
  }, []);

  useEffect(() => {
    if (!selectedCarId) {
      setCarVariants([]);
      return;
    }
    listVariantsForCar(selectedCarId).then(setCarVariants).catch(() => setCarVariants([]));
  }, [selectedCarId]);

  function addToComparison() {
    if (!selectedVariantId) return;
    const variant = carVariants.find((v) => v.id === Number(selectedVariantId));
    const car = cars.find((c) => c.id === Number(selectedCarId));
    if (!variant || picked.some((p) => p.variant_id === variant.id)) return;
    setPicked((p) => [...p, { variant_id: variant.id, car_model: car?.model, variant_name: variant.variant_name }]);
  }

  function removePicked(id) {
    setPicked((p) => p.filter((x) => x.variant_id !== id));
    setRows(null);
  }

  async function runCompare() {
    setError("");
    try {
      const data = await compareVariants(picked.map((p) => p.variant_id));
      setRows(data);
    } catch {
      setError("Comparison failed — need at least 2 variants.");
    }
  }

  return (
    <div>
      <header className="mb-6">
        <h1 className="font-display font-semibold text-2xl">Compare vehicles</h1>
        <p className="text-ink-soft text-sm mt-1">Pick 2–10 variants to see them side by side.</p>
      </header>

      <div className="bg-surface border border-line rounded-lg p-5 mb-6">
        <div className="flex flex-wrap items-end gap-3">
          <label className="flex flex-col gap-1 text-sm">
            <span className="font-medium">Car</span>
            <select
              className="border border-line rounded-md px-3 py-2 bg-surface min-w-[180px]"
              value={selectedCarId}
              onChange={(e) => {
                setSelectedCarId(e.target.value);
                setSelectedVariantId("");
              }}
            >
              <option value="">Select a car</option>
              {cars.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.model}
                </option>
              ))}
            </select>
          </label>
          <label className="flex flex-col gap-1 text-sm">
            <span className="font-medium">Variant</span>
            <select
              className="border border-line rounded-md px-3 py-2 bg-surface min-w-[160px]"
              value={selectedVariantId}
              onChange={(e) => setSelectedVariantId(e.target.value)}
              disabled={!selectedCarId}
            >
              <option value="">Select a variant</option>
              {carVariants.map((v) => (
                <option key={v.id} value={v.id}>
                  {v.variant_name}
                </option>
              ))}
            </select>
          </label>
          <button
            type="button"
            onClick={addToComparison}
            disabled={!selectedVariantId}
            className="bg-primary text-white text-sm font-medium px-4 py-2 rounded-md hover:bg-primary-soft disabled:opacity-50"
          >
            Add to comparison
          </button>
        </div>

        {picked.length > 0 && (
          <div className="flex flex-wrap gap-2 mt-4">
            {picked.map((p) => (
              <span key={p.variant_id} className="text-xs bg-accent-soft text-accent px-2 py-1 rounded-full flex items-center gap-2">
                {p.car_model} · {p.variant_name}
                <button onClick={() => removePicked(p.variant_id)} aria-label={`Remove ${p.car_model} ${p.variant_name}`}>
                  ×
                </button>
              </span>
            ))}
          </div>
        )}

        <button
          type="button"
          onClick={runCompare}
          disabled={picked.length < 2}
          className="mt-4 bg-ink text-white text-sm font-medium px-4 py-2 rounded-md disabled:opacity-40"
        >
          Compare {picked.length >= 2 ? `(${picked.length})` : ""}
        </button>
      </div>

      {error && <div className="mb-6 text-sm text-danger bg-caution-soft border border-caution rounded-md px-4 py-3">{error}</div>}

      {cars.length === 0 && !error && (
        <EmptyState
          title="No cars in the catalog yet"
          description="Add manufacturers, cars, and variants from the Catalog page to start comparing."
          action={
            <Link to="/catalog" className="text-primary font-medium hover:underline text-sm">
              Go to Catalog &rarr;
            </Link>
          }
        />
      )}

      {rows && (
        <div className="overflow-x-auto bg-surface border border-line rounded-lg">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-line">
                <th className="text-left p-3 font-medium text-ink-soft">Spec</th>
                {rows.map((r) => (
                  <th key={r.variant_id} className="text-left p-3 font-display font-semibold">
                    {r.manufacturer_name} {r.car_model}
                    <div className="text-xs text-ink-soft font-body font-normal">{r.variant_name}</div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {ROWS.map((row) => (
                <tr key={row.key} className="border-b border-line last:border-0">
                  <td className="p-3 text-ink-soft">{row.label}</td>
                  {rows.map((r) => (
                    <td key={r.variant_id} className="p-3 font-data">
                      {row.fmt(r[row.key])}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
