import { useEffect, useState } from "react";
import {
  listManufacturers,
  createManufacturer,
  deleteManufacturer,
  listCars,
  createCar,
  deleteCar,
  listVariantsForCar,
  createVariant,
  deleteVariant,
} from "../api/client";
import { useAuth } from "../context/AuthContext";
import SectionHeading from "../components/ui/SectionHeading";
import SolidCard from "../components/ui/SolidCard";
import Badge from "../components/ui/Badge";
import Button from "../components/ui/Button";
import LoginForm from "../components/LoginForm";
import ErrorAlert from "../components/ui/ErrorAlert";
import { Database, ShieldCheck, Plus, Trash2 } from "lucide-react";

const TABS = ["Manufacturers", "Cars", "Variants"];

export default function CatalogPage() {
  const { user } = useAuth();
  const [tab, setTab] = useState("Manufacturers");
  const [manufacturers, setManufacturers] = useState([]);
  const [cars, setCars] = useState([]);
  const [error, setError] = useState("");

  function refreshManufacturers() {
    listManufacturers({ limit: 500 }).then(setManufacturers).catch(() => setError("Couldn't load manufacturers."));
  }
  function refreshCars() {
    listCars({ limit: 500 }).then(setCars).catch(() => setError("Couldn't load cars."));
  }

  useEffect(() => {
    refreshManufacturers();
    refreshCars();
  }, []);

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 md:py-12 space-y-8 animate-fade-in">
      <SectionHeading
        badge={<Badge variant="cyan" icon={Database}>Catalog & Pipelines</Badge>}
        title="Vehicle Catalog Ingestion & Management"
        subtitle="Manage manufacturers, vehicle models, variants, and data scraper sources."
      />

      {/* Tabs Bar */}
      <div className="flex gap-2 border-b border-[var(--color-line)] pb-2">
        {TABS.map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-2 text-sm font-semibold rounded-xl transition-all button-press ${
              tab === t
                ? "bg-[var(--color-primary)] text-white shadow-sm"
                : "text-[var(--color-text-muted)] hover:text-white hover:bg-white/5"
            }`}
          >
            {t}
          </button>
        ))}
      </div>

      {error && <ErrorAlert title="Catalog Error" message={error} />}

      {!user && (
        <SolidCard className="border border-[var(--color-line-bright)]">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div>
              <h4 className="text-sm font-bold text-white flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-400" /> Admin Access Gated
              </h4>
              <p className="text-xs text-[var(--color-text-muted)] mt-0.5">
                Browsing is open to all visitors. Sign in as admin to add, edit, or remove catalog records.
              </p>
            </div>
            <LoginForm />
          </div>
        </SolidCard>
      )}

      {tab === "Manufacturers" && (
        <ManufacturersTab manufacturers={manufacturers} onChange={refreshManufacturers} canEdit={!!user} />
      )}
      {tab === "Cars" && (
        <CarsTab cars={cars} manufacturers={manufacturers} onChange={refreshCars} canEdit={!!user} />
      )}
      {tab === "Variants" && <VariantsTab cars={cars} canEdit={!!user} />}
    </div>
  );
}

// --- Manufacturers Tab ---
function ManufacturersTab({ manufacturers, onChange, canEdit }) {
  const [name, setName] = useState("");
  const [website, setWebsite] = useState("");
  const [country, setCountry] = useState("");

  async function handleAdd(e) {
    e.preventDefault();
    if (!name.trim()) return;
    await createManufacturer({ name, website: website || null, country: country || null });
    setName("");
    setWebsite("");
    setCountry("");
    onChange();
  }

  return (
    <div className="space-y-6">
      {canEdit && (
        <SolidCard className="border border-[var(--color-line-bright)]">
          <h4 className="text-sm font-bold text-white mb-3 flex items-center gap-1.5">
            <Plus className="w-4 h-4 text-cyan-400" /> Add Manufacturer
          </h4>
          <form onSubmit={handleAdd} className="flex flex-wrap gap-3 items-end">
            <label className="flex flex-col gap-1 text-xs min-w-[180px]">
              <span className="font-medium text-[var(--color-text-muted)]">Name</span>
              <input required className="bg-[var(--color-surface-subtle)] border border-[var(--color-line)] rounded-xl px-3 py-2 text-sm text-white" value={name} onChange={(e) => setName(e.target.value)} />
            </label>
            <label className="flex flex-col gap-1 text-xs min-w-[150px]">
              <span className="font-medium text-[var(--color-text-muted)]">Country</span>
              <input className="bg-[var(--color-surface-subtle)] border border-[var(--color-line)] rounded-xl px-3 py-2 text-sm text-white" value={country} onChange={(e) => setCountry(e.target.value)} />
            </label>
            <label className="flex flex-col gap-1 text-xs min-w-[200px]">
              <span className="font-medium text-[var(--color-text-muted)]">Website</span>
              <input className="bg-[var(--color-surface-subtle)] border border-[var(--color-line)] rounded-xl px-3 py-2 text-sm text-white" value={website} onChange={(e) => setWebsite(e.target.value)} />
            </label>
            <Button type="submit" variant="primary" size="md" icon={Plus}>
              Save Manufacturer
            </Button>
          </form>
        </SolidCard>
      )}

      <SolidCard className="p-0 overflow-hidden border border-[var(--color-line-bright)]">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead>
              <tr className="bg-[var(--color-surface-subtle)] border-b border-[var(--color-line)] text-xs text-[var(--color-text-muted)] uppercase tracking-wider">
                <th className="p-4">Name</th>
                <th className="p-4">Country</th>
                <th className="p-4">Data Source Type</th>
                <th className="p-4">Trust Score</th>
                {canEdit && <th className="p-4 text-right">Actions</th>}
              </tr>
            </thead>
            <tbody className="divide-y divide-[var(--color-line)]">
              {manufacturers.map((m) => (
                <tr key={m.id} className="hover:bg-white/[0.02]">
                  <td className="p-4 font-bold text-white">{m.name}</td>
                  <td className="p-4 text-[var(--color-text-muted)]">{m.country ?? "—"}</td>
                  <td className="p-4">
                    <Badge variant={m.data_source_type === "scraper" ? "cyan" : "primary"}>
                      {m.data_source_type || "manual"}
                    </Badge>
                  </td>
                  <td className="p-4 font-mono text-emerald-400 font-semibold">{m.confidence_score != null ? `${m.confidence_score}%` : "—"}</td>
                  {canEdit && (
                    <td className="p-4 text-right">
                      <button
                        onClick={async () => {
                          await deleteManufacturer(m.id);
                          onChange();
                        }}
                        className="text-red-400 hover:text-red-300 text-xs flex items-center gap-1 ml-auto"
                      >
                        <Trash2 className="w-3.5 h-3.5" /> Delete
                      </button>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </SolidCard>
    </div>
  );
}

// --- Cars Tab ---
function CarsTab({ cars, manufacturers, onChange, canEdit }) {
  const [model, setModel] = useState("");
  const [bodyType, setBodyType] = useState("");
  const [launchYear, setLaunchYear] = useState("");
  const [manufacturerId, setManufacturerId] = useState("");

  async function handleAdd(e) {
    e.preventDefault();
    if (!model.trim() || !manufacturerId) return;
    await createCar({
      model,
      body_type: bodyType || null,
      launch_year: launchYear ? Number(launchYear) : null,
      manufacturer_id: Number(manufacturerId),
    });
    setModel("");
    setBodyType("");
    setLaunchYear("");
    onChange();
  }

  const manufacturerName = (id) => manufacturers.find((m) => m.id === id)?.name ?? id;

  return (
    <div className="space-y-6">
      {canEdit && (
        <SolidCard className="border border-[var(--color-line-bright)]">
          <h4 className="text-sm font-bold text-white mb-3 flex items-center gap-1.5">
            <Plus className="w-4 h-4 text-cyan-400" /> Add Vehicle Model
          </h4>
          <form onSubmit={handleAdd} className="flex flex-wrap gap-3 items-end">
            <label className="flex flex-col gap-1 text-xs min-w-[180px]">
              <span className="font-medium text-[var(--color-text-muted)]">Manufacturer</span>
              <select required className="bg-[var(--color-surface-subtle)] border border-[var(--color-line)] rounded-xl px-3 py-2 text-sm text-white" value={manufacturerId} onChange={(e) => setManufacturerId(e.target.value)}>
                <option value="">Select Manufacturer</option>
                {manufacturers.map((m) => (
                  <option key={m.id} value={m.id}>{m.name}</option>
                ))}
              </select>
            </label>
            <label className="flex flex-col gap-1 text-xs min-w-[180px]">
              <span className="font-medium text-[var(--color-text-muted)]">Model Name</span>
              <input required className="bg-[var(--color-surface-subtle)] border border-[var(--color-line)] rounded-xl px-3 py-2 text-sm text-white" value={model} onChange={(e) => setModel(e.target.value)} />
            </label>
            <label className="flex flex-col gap-1 text-xs min-w-[150px]">
              <span className="font-medium text-[var(--color-text-muted)]">Body Type</span>
              <select className="bg-[var(--color-surface-subtle)] border border-[var(--color-line)] rounded-xl px-3 py-2 text-sm text-white" value={bodyType} onChange={(e) => setBodyType(e.target.value)}>
                <option value="">Select</option>
                <option value="Hatchback">Hatchback</option>
                <option value="Sedan">Sedan</option>
                <option value="SUV">SUV</option>
                <option value="MPV">MPV</option>
              </select>
            </label>
            <Button type="submit" variant="primary" size="md" icon={Plus}>
              Save Model
            </Button>
          </form>
        </SolidCard>
      )}

      <SolidCard className="p-0 overflow-hidden border border-[var(--color-line-bright)]">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead>
              <tr className="bg-[var(--color-surface-subtle)] border-b border-[var(--color-line)] text-xs text-[var(--color-text-muted)] uppercase tracking-wider">
                <th className="p-4">Model</th>
                <th className="p-4">Manufacturer</th>
                <th className="p-4">Body Type</th>
                {canEdit && <th className="p-4 text-right">Actions</th>}
              </tr>
            </thead>
            <tbody className="divide-y divide-[var(--color-line)]">
              {cars.map((c) => (
                <tr key={c.id} className="hover:bg-white/[0.02]">
                  <td className="p-4 font-bold text-white">{c.model}</td>
                  <td className="p-4 text-cyan-400 font-medium">{manufacturerName(c.manufacturer_id)}</td>
                  <td className="p-4 text-[var(--color-text-muted)]">{c.body_type ?? "—"}</td>
                  {canEdit && (
                    <td className="p-4 text-right">
                      <button
                        onClick={async () => {
                          await deleteCar(c.id);
                          onChange();
                        }}
                        className="text-red-400 hover:text-red-300 text-xs flex items-center gap-1 ml-auto"
                      >
                        <Trash2 className="w-3.5 h-3.5" /> Delete
                      </button>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </SolidCard>
    </div>
  );
}

// --- Variants Tab ---
function VariantsTab({ cars, canEdit }) {
  const [carId, setCarId] = useState("");
  const [variants, setVariants] = useState([]);

  useEffect(() => {
    if (carId) {
      listVariantsForCar(carId).then(setVariants).catch(() => setVariants([]));
    }
  }, [carId]);

  return (
    <div className="space-y-6">
      <SolidCard className="border border-[var(--color-line-bright)] max-w-md">
        <label className="flex flex-col gap-1.5 text-xs font-medium text-[var(--color-text-muted)]">
          <span>Select Model to View Variants</span>
          <select
            className="bg-[var(--color-surface-subtle)] border border-[var(--color-line)] rounded-xl px-3.5 py-2.5 text-sm text-white"
            value={carId}
            onChange={(e) => setCarId(e.target.value)}
          >
            <option value="">Select a Car Model</option>
            {cars.map((c) => (
              <option key={c.id} value={c.id}>{c.model}</option>
            ))}
          </select>
        </label>
      </SolidCard>

      {carId && (
        <SolidCard className="p-0 overflow-hidden border border-[var(--color-line-bright)]">
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead>
                <tr className="bg-[var(--color-surface-subtle)] border-b border-[var(--color-line)] text-xs text-[var(--color-text-muted)] uppercase tracking-wider">
                  <th className="p-4">Variant Name</th>
                  <th className="p-4">Price</th>
                  <th className="p-4">Fuel</th>
                  <th className="p-4">Transmission</th>
                  {canEdit && <th className="p-4 text-right">Actions</th>}
                </tr>
              </thead>
              <tbody className="divide-y divide-[var(--color-line)]">
                {variants.map((v) => (
                  <tr key={v.id} className="hover:bg-white/[0.02]">
                    <td className="p-4 font-bold text-white">{v.variant_name}</td>
                    <td className="p-4 font-mono text-emerald-400 font-semibold">
                      {v.price != null ? `₹${v.price.toLocaleString("en-IN")}` : "—"}
                    </td>
                    <td className="p-4 text-[var(--color-text-muted)]">{v.fuel ?? "—"}</td>
                    <td className="p-4 text-[var(--color-text-muted)]">{v.transmission ?? "—"}</td>
                    {canEdit && (
                      <td className="p-4 text-right">
                        <button
                          onClick={async () => {
                            await deleteVariant(v.id);
                            listVariantsForCar(carId).then(setVariants);
                          }}
                          className="text-red-400 hover:text-red-300 text-xs flex items-center gap-1 ml-auto"
                        >
                          <Trash2 className="w-3.5 h-3.5" /> Delete
                        </button>
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </SolidCard>
      )}
    </div>
  );
}
