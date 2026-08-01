import { useEffect, useState } from "react";
import { listCars, listVariantsForCar } from "../../api/client";
import { Plus, X, ArrowRightLeft } from "lucide-react";
import Button from "../ui/Button";
import SolidCard from "../ui/SolidCard";
import Badge from "../ui/Badge";

export default function VariantSelector({ picked, setPicked, onCompare, loading }) {
  const [cars, setCars] = useState([]);
  const [selectedCarId, setSelectedCarId] = useState("");
  const [carVariants, setCarVariants] = useState([]);
  const [selectedVariantId, setSelectedVariantId] = useState("");

  useEffect(() => {
    listCars({ limit: 500 }).then(setCars).catch(() => {});
  }, []);

  useEffect(() => {
    if (!selectedCarId) {
      setCarVariants([]);
      return;
    }
    listVariantsForCar(selectedCarId).then(setCarVariants).catch(() => setCarVariants([]));
  }, [selectedCarId]);

  function handleAdd() {
    if (!selectedVariantId) return;
    const variant = carVariants.find((v) => v.id === Number(selectedVariantId));
    const car = cars.find((c) => c.id === Number(selectedCarId));
    if (!variant || picked.some((p) => p.variant_id === variant.id)) return;
    setPicked((p) => [...p, { variant_id: variant.id, car_model: car?.model, variant_name: variant.variant_name }]);
  }

  function handleRemove(id) {
    setPicked((p) => p.filter((x) => x.variant_id !== id));
  }

  return (
    <SolidCard className="space-y-4 border border-[var(--color-line-bright)]">
      <div className="flex flex-wrap items-end gap-3">
        <label className="flex flex-col gap-1.5 flex-1 min-w-[200px]">
          <span className="text-xs font-medium text-[var(--color-text-muted)]">Select Model</span>
          <select
            value={selectedCarId}
            onChange={(e) => {
              setSelectedCarId(e.target.value);
              setSelectedVariantId("");
            }}
            className="w-full bg-[var(--color-surface-subtle)] border border-[var(--color-line)] rounded-xl px-3.5 py-2.5 text-sm text-white focus:border-[var(--color-primary)]"
          >
            <option value="">Select a car model</option>
            {cars.map((c) => (
              <option key={c.id} value={c.id}>
                {c.model}
              </option>
            ))}
          </select>
        </label>

        <label className="flex flex-col gap-1.5 flex-1 min-w-[200px]">
          <span className="text-xs font-medium text-[var(--color-text-muted)]">Select Variant</span>
          <select
            value={selectedVariantId}
            onChange={(e) => setSelectedVariantId(e.target.value)}
            disabled={!selectedCarId || carVariants.length === 0}
            className="w-full bg-[var(--color-surface-subtle)] border border-[var(--color-line)] rounded-xl px-3.5 py-2.5 text-sm text-white disabled:opacity-50 focus:border-[var(--color-primary)]"
          >
            <option value="">Select variant</option>
            {carVariants.map((v) => (
              <option key={v.id} value={v.id}>
                {v.variant_name} ({v.price ? `₹${(v.price/100000).toFixed(1)}L` : 'Price N/A'})
              </option>
            ))}
          </select>
        </label>

        <Button
          variant="secondary"
          disabled={!selectedVariantId}
          onClick={handleAdd}
          icon={Plus}
        >
          Add Variant
        </Button>
      </div>

      {/* Selected Variant Chips */}
      {picked.length > 0 && (
        <div className="pt-2 flex flex-wrap gap-2">
          {picked.map((p) => (
            <span
              key={p.variant_id}
              className="inline-flex items-center gap-2 text-xs font-medium bg-[var(--color-primary-soft)] text-indigo-200 border border-[var(--color-primary)]/30 px-3 py-1.5 rounded-full"
            >
              <strong>{p.car_model}</strong> · {p.variant_name}
              <button
                type="button"
                onClick={() => handleRemove(p.variant_id)}
                className="text-indigo-400 hover:text-white rounded-full p-0.5 focus:outline-none"
                aria-label={`Remove ${p.car_model} ${p.variant_name}`}
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </span>
          ))}
        </div>
      )}

      {/* Run Comparison CTA */}
      <div className="pt-2 flex items-center justify-between">
        <span className="text-xs text-[var(--color-text-dim)] font-mono">
          Pick 2 to 10 variants for side-by-side spec matrix
        </span>
        <Button
          variant="cyan"
          disabled={picked.length < 2 || loading}
          loading={loading}
          onClick={onCompare}
          icon={ArrowRightLeft}
        >
          Compare {picked.length >= 2 ? `(${picked.length} Vehicles)` : ""}
        </Button>
      </div>
    </SolidCard>
  );
}
