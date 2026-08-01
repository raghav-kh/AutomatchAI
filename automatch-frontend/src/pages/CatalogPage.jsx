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
import LoginForm from "../components/LoginForm";

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
    <div>
      <header className="mb-6">
        <h1 className="font-display font-semibold text-2xl">Catalog</h1>
        <p className="text-ink-soft text-sm mt-1">Manage manufacturers, cars, and variants directly.</p>
      </header>

      <div className="flex gap-1 mb-5 border-b border-line">
        {TABS.map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={`px-4 py-2 text-sm font-medium border-b-2 -mb-px transition-colors ${
              tab === t ? "border-primary text-primary" : "border-transparent text-ink-soft hover:text-ink"
            }`}
          >
            {t}
          </button>
        ))}
      </div>

      {error && <div className="mb-4 text-sm text-danger bg-caution-soft border border-caution rounded-md px-4 py-3">{error}</div>}

      {!user && (
        <div className="mb-5">
          <p className="text-sm text-ink-soft mb-2">Browsing is open to everyone. Sign in to add, edit, or delete catalog entries.</p>
          <LoginForm />
        </div>
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

// --- Manufacturers ---
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
    <div>
      {canEdit && (
        <form onSubmit={handleAdd} className="bg-surface border border-line rounded-lg p-4 flex flex-wrap gap-3 items-end mb-5">
          <label className="flex flex-col gap-1 text-sm">
            <span className="font-medium">Name</span>
            <input required className="border border-line rounded-md px-3 py-2" value={name} onChange={(e) => setName(e.target.value)} />
          </label>
          <label className="flex flex-col gap-1 text-sm">
            <span className="font-medium">Country</span>
            <input className="border border-line rounded-md px-3 py-2" value={country} onChange={(e) => setCountry(e.target.value)} />
          </label>
          <label className="flex flex-col gap-1 text-sm">
            <span className="font-medium">Website</span>
            <input className="border border-line rounded-md px-3 py-2" value={website} onChange={(e) => setWebsite(e.target.value)} />
          </label>
          <button type="submit" className="bg-primary text-white text-sm font-medium px-4 py-2 rounded-md hover:bg-primary-soft">
            Add manufacturer
          </button>
        </form>
      )}

      <div className="bg-surface border border-line rounded-lg overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-line text-left text-ink-soft">
              <th className="p-3 font-medium">Name</th>
              <th className="p-3 font-medium">Country</th>
              <th className="p-3 font-medium">Source type</th>
              <th className="p-3 font-medium">Confidence</th>
              {canEdit && <th className="p-3"></th>}
            </tr>
          </thead>
          <tbody>
            {manufacturers.map((m) => (
              <tr key={m.id} className="border-b border-line last:border-0">
                <td className="p-3 font-medium">{m.name}</td>
                <td className="p-3 text-ink-soft">{m.country ?? "—"}</td>
                <td className="p-3 text-ink-soft">{m.data_source_type}</td>
                <td className="p-3 font-data text-ink-soft">{m.confidence_score != null ? m.confidence_score : "—"}</td>
                {canEdit && (
                  <td className="p-3 text-right">
                    <button
                      onClick={async () => {
                        await deleteManufacturer(m.id);
                        onChange();
                      }}
                      className="text-danger text-xs hover:underline"
                    >
                      Delete
                    </button>
                  </td>
                )}
              </tr>
            ))}
            {manufacturers.length === 0 && (
              <tr>
                <td colSpan={5} className="p-6 text-center text-ink-soft">
                  No manufacturers yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// --- Cars ---
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
    <div>
      {canEdit && (
      <form onSubmit={handleAdd} className="bg-surface border border-line rounded-lg p-4 flex flex-wrap gap-3 items-end mb-5">
        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium">Manufacturer</span>
          <select
            required
            className="border border-line rounded-md px-3 py-2 bg-surface"
            value={manufacturerId}
            onChange={(e) => setManufacturerId(e.target.value)}
          >
            <option value="">Select</option>
            {manufacturers.map((m) => (
              <option key={m.id} value={m.id}>
                {m.name}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium">Model</span>
          <input required className="border border-line rounded-md px-3 py-2" value={model} onChange={(e) => setModel(e.target.value)} />
        </label>
        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium">Body type</span>
          <select className="border border-line rounded-md px-3 py-2 bg-surface" value={bodyType} onChange={(e) => setBodyType(e.target.value)}>
            <option value="">—</option>
            <option value="Hatchback">Hatchback</option>
            <option value="Sedan">Sedan</option>
            <option value="SUV">SUV</option>
            <option value="MPV">MPV</option>
          </select>
        </label>
        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium">Launch year</span>
          <input type="number" className="border border-line rounded-md px-3 py-2 w-24" value={launchYear} onChange={(e) => setLaunchYear(e.target.value)} />
        </label>
        <button type="submit" className="bg-primary text-white text-sm font-medium px-4 py-2 rounded-md hover:bg-primary-soft">
          Add car
        </button>
      </form>
      )}

      <div className="bg-surface border border-line rounded-lg overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-line text-left text-ink-soft">
              <th className="p-3 font-medium">Model</th>
              <th className="p-3 font-medium">Manufacturer</th>
              <th className="p-3 font-medium">Body type</th>
              <th className="p-3 font-medium">Year</th>
              {canEdit && <th className="p-3"></th>}
            </tr>
          </thead>
          <tbody>
            {cars.map((c) => (
              <tr key={c.id} className="border-b border-line last:border-0">
                <td className="p-3 font-medium">{c.model}</td>
                <td className="p-3 text-ink-soft">{manufacturerName(c.manufacturer_id)}</td>
                <td className="p-3 text-ink-soft">{c.body_type ?? "—"}</td>
                <td className="p-3 text-ink-soft">{c.launch_year ?? "—"}</td>
                {canEdit && (
                  <td className="p-3 text-right">
                    <button
                      onClick={async () => {
                        await deleteCar(c.id);
                        onChange();
                      }}
                      className="text-danger text-xs hover:underline"
                    >
                      Delete
                    </button>
                  </td>
                )}
              </tr>
            ))}
            {cars.length === 0 && (
              <tr>
                <td colSpan={5} className="p-6 text-center text-ink-soft">
                  No cars yet. Add a manufacturer first, then a car.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

// --- Variants ---
const EMPTY_VARIANT_FORM = {
  variant_name: "",
  price: "",
  fuel: "",
  transmission: "",
  mileage: "",
  safety_rating: "",
  seating: "",
  length: "",
  boot_space: "",
  family_score: "",
  city_friendliness: "",
  highway_comfort: "",
  maintenance_level: "",
  resale_value: "",
  service_network: "",
};

function VariantsTab({ cars, canEdit }) {
  const [carId, setCarId] = useState("");
  const [variants, setVariants] = useState([]);
  const [form, setForm] = useState(EMPTY_VARIANT_FORM);

  function refresh(id) {
    if (!id) {
      setVariants([]);
      return;
    }
    listVariantsForCar(id).then(setVariants).catch(() => setVariants([]));
  }

  useEffect(() => refresh(carId), [carId]);

  function set(field, value) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  function num(value) {
    return value === "" ? undefined : Number(value);
  }

  async function handleAdd(e) {
    e.preventDefault();
    if (!carId || !form.variant_name.trim()) return;

    const hasSpec = ["safety_rating", "seating", "length", "boot_space"].some((k) => form[k] !== "");
    const hasAi = ["family_score", "city_friendliness", "highway_comfort", "maintenance_level", "resale_value", "service_network"].some(
      (k) => form[k] !== ""
    );

    await createVariant(carId, {
      variant_name: form.variant_name,
      price: num(form.price),
      fuel: form.fuel || undefined,
      transmission: form.transmission || undefined,
      mileage: num(form.mileage),
      specifications: hasSpec
        ? {
            safety_rating: num(form.safety_rating),
            seating: num(form.seating),
            length: num(form.length),
            boot_space: num(form.boot_space),
          }
        : undefined,
      ai_attributes: hasAi
        ? {
            family_score: num(form.family_score),
            city_friendliness: num(form.city_friendliness),
            highway_comfort: num(form.highway_comfort),
            maintenance_level: num(form.maintenance_level),
            resale_value: num(form.resale_value),
            service_network: num(form.service_network),
          }
        : undefined,
    });
    setForm(EMPTY_VARIANT_FORM);
    refresh(carId);
  }

  return (
    <div>
      <label className="flex flex-col gap-1 text-sm mb-4 max-w-xs">
        <span className="font-medium">Car</span>
        <select className="border border-line rounded-md px-3 py-2 bg-surface" value={carId} onChange={(e) => setCarId(e.target.value)}>
          <option value="">Select a car</option>
          {cars.map((c) => (
            <option key={c.id} value={c.id}>
              {c.model}
            </option>
          ))}
        </select>
      </label>

      {carId && (
        <>
          {canEdit && (
          <form onSubmit={handleAdd} className="bg-surface border border-line rounded-lg p-4 mb-5">
            <div className="grid sm:grid-cols-3 gap-3">
              <Field label="Variant name" value={form.variant_name} onChange={(v) => set("variant_name", v)} required />
              <Field label="Price (₹)" type="number" value={form.price} onChange={(v) => set("price", v)} />
              <SelectField label="Fuel" value={form.fuel} onChange={(v) => set("fuel", v)} options={["Petrol", "Diesel", "CNG", "Electric", "Hybrid"]} />
              <SelectField label="Transmission" value={form.transmission} onChange={(v) => set("transmission", v)} options={["Manual", "Automatic"]} />
              <Field label="Mileage (km/l or km/kWh)" type="number" value={form.mileage} onChange={(v) => set("mileage", v)} />
              <Field label="Safety rating (0-5)" type="number" value={form.safety_rating} onChange={(v) => set("safety_rating", v)} />
              <Field label="Seating" type="number" value={form.seating} onChange={(v) => set("seating", v)} />
              <Field label="Length (mm)" type="number" value={form.length} onChange={(v) => set("length", v)} />
              <Field label="Boot space (L)" type="number" value={form.boot_space} onChange={(v) => set("boot_space", v)} />
              <Field label="Family score (0-10)" type="number" value={form.family_score} onChange={(v) => set("family_score", v)} />
              <Field label="City friendliness (0-10)" type="number" value={form.city_friendliness} onChange={(v) => set("city_friendliness", v)} />
              <Field label="Highway comfort (0-10)" type="number" value={form.highway_comfort} onChange={(v) => set("highway_comfort", v)} />
              <Field label="Maintenance level (0-10)" type="number" value={form.maintenance_level} onChange={(v) => set("maintenance_level", v)} />
              <Field label="Resale value (0-10)" type="number" value={form.resale_value} onChange={(v) => set("resale_value", v)} />
              <Field label="Service network (0-10)" type="number" value={form.service_network} onChange={(v) => set("service_network", v)} />
            </div>
            <button type="submit" className="mt-4 bg-primary text-white text-sm font-medium px-4 py-2 rounded-md hover:bg-primary-soft">
              Add variant
            </button>
          </form>
          )}

          <div className="bg-surface border border-line rounded-lg overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-line text-left text-ink-soft">
                  <th className="p-3 font-medium">Variant</th>
                  <th className="p-3 font-medium">Price</th>
                  <th className="p-3 font-medium">Fuel</th>
                  <th className="p-3 font-medium">Transmission</th>
                  {canEdit && <th className="p-3"></th>}
                </tr>
              </thead>
              <tbody>
                {variants.map((v) => (
                  <tr key={v.id} className="border-b border-line last:border-0">
                    <td className="p-3 font-medium">{v.variant_name}</td>
                    <td className="p-3 font-data">{v.price != null ? `₹${v.price.toLocaleString("en-IN")}` : "—"}</td>
                    <td className="p-3 text-ink-soft">{v.fuel ?? "—"}</td>
                    <td className="p-3 text-ink-soft">{v.transmission ?? "—"}</td>
                    {canEdit && (
                      <td className="p-3 text-right">
                        <button
                          onClick={async () => {
                            await deleteVariant(v.id);
                            refresh(carId);
                          }}
                          className="text-danger text-xs hover:underline"
                        >
                          Delete
                        </button>
                      </td>
                    )}
                  </tr>
                ))}
                {variants.length === 0 && (
                  <tr>
                    <td colSpan={5} className="p-6 text-center text-ink-soft">
                      No variants for this car yet.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}

function Field({ label, value, onChange, type = "text", required = false }) {
  return (
    <label className="flex flex-col gap-1 text-sm">
      <span className="font-medium">{label}</span>
      <input
        type={type}
        required={required}
        className="border border-line rounded-md px-3 py-2"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </label>
  );
}

function SelectField({ label, value, onChange, options }) {
  return (
    <label className="flex flex-col gap-1 text-sm">
      <span className="font-medium">{label}</span>
      <select className="border border-line rounded-md px-3 py-2 bg-surface" value={value} onChange={(e) => onChange(e.target.value)}>
        <option value="">—</option>
        {options.map((o) => (
          <option key={o} value={o}>
            {o}
          </option>
        ))}
      </select>
    </label>
  );
}
