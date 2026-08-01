import { useState } from "react";
import { getRecommendations } from "../api/client";
import RecommendationCard from "../components/RecommendationCard";
import EmptyState from "../components/EmptyState";
import { Link } from "react-router-dom";

const DEFAULT_PREFS = {
  budget: 1000000,
  family_members: "",
  daily_running_km: "",
  highway_usage: "occasional",
  fuel_preference: "",
  transmission_preference: "",
  body_type_preference: "",
  service_availability_importance: 3,
  safety_importance: 3,
  parking_constraint: "normal",
  elderly_passengers: false,
  beginner_driver: false,
};

function cleanPayload(prefs) {
  const payload = { ...prefs };
  for (const key of ["family_members", "daily_running_km", "fuel_preference", "transmission_preference", "body_type_preference"]) {
    if (payload[key] === "") delete payload[key];
  }
  payload.budget = Number(payload.budget);
  if (payload.family_members !== undefined) payload.family_members = Number(payload.family_members);
  if (payload.daily_running_km !== undefined) payload.daily_running_km = Number(payload.daily_running_km);
  payload.service_availability_importance = Number(payload.service_availability_importance);
  payload.safety_importance = Number(payload.safety_importance);
  return payload;
}

export default function RecommendPage() {
  const [prefs, setPrefs] = useState(DEFAULT_PREFS);
  const [results, setResults] = useState(null);
  const [status, setStatus] = useState("idle"); // idle | loading | error
  const [errorMsg, setErrorMsg] = useState("");

  function set(field, value) {
    setPrefs((p) => ({ ...p, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setStatus("loading");
    setErrorMsg("");
    try {
      const data = await getRecommendations(cleanPayload(prefs), 10);
      setResults(data);
      setStatus("idle");
    } catch (err) {
      setStatus("error");
      setErrorMsg(err?.response?.data?.detail ? JSON.stringify(err.response.data.detail) : "Couldn't reach the API. Check VITE_API_BASE_URL and that the backend is running.");
    }
  }

  return (
    <div>
      <header className="mb-6">
        <h1 className="font-display font-semibold text-2xl">Find your car</h1>
        <p className="text-ink-soft text-sm mt-1">
          Answer a few questions instead of filtering specs — AutoMatch AI ranks vehicles for your actual life.
        </p>
      </header>

      <form onSubmit={handleSubmit} className="bg-surface border border-line rounded-lg p-5 grid sm:grid-cols-2 gap-4 mb-8">
        <label className="flex flex-col gap-1 text-sm sm:col-span-2">
          <span className="font-medium">Budget (₹, ex-showroom)</span>
          <input
            type="number"
            required
            min={1}
            className="border border-line rounded-md px-3 py-2 font-data"
            value={prefs.budget}
            onChange={(e) => set("budget", e.target.value)}
          />
        </label>

        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium">Family members</span>
          <input
            type="number"
            min={1}
            max={10}
            placeholder="e.g. 4"
            className="border border-line rounded-md px-3 py-2"
            value={prefs.family_members}
            onChange={(e) => set("family_members", e.target.value)}
          />
        </label>

        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium">Daily driving (km)</span>
          <input
            type="number"
            min={0}
            placeholder="e.g. 20"
            className="border border-line rounded-md px-3 py-2"
            value={prefs.daily_running_km}
            onChange={(e) => set("daily_running_km", e.target.value)}
          />
        </label>

        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium">Highway usage</span>
          <select
            className="border border-line rounded-md px-3 py-2 bg-surface"
            value={prefs.highway_usage}
            onChange={(e) => set("highway_usage", e.target.value)}
          >
            <option value="rare">Rare</option>
            <option value="occasional">Occasional</option>
            <option value="frequent">Frequent</option>
          </select>
        </label>

        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium">Body type</span>
          <select
            className="border border-line rounded-md px-3 py-2 bg-surface"
            value={prefs.body_type_preference}
            onChange={(e) => set("body_type_preference", e.target.value)}
          >
            <option value="">No preference</option>
            <option value="Hatchback">Hatchback</option>
            <option value="Sedan">Sedan</option>
            <option value="SUV">SUV</option>
            <option value="MPV">MPV</option>
          </select>
        </label>

        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium">Fuel preference</span>
          <select
            className="border border-line rounded-md px-3 py-2 bg-surface"
            value={prefs.fuel_preference}
            onChange={(e) => set("fuel_preference", e.target.value)}
          >
            <option value="">No preference</option>
            <option value="Petrol">Petrol</option>
            <option value="Diesel">Diesel</option>
            <option value="CNG">CNG</option>
            <option value="Electric">Electric</option>
            <option value="Hybrid">Hybrid</option>
          </select>
        </label>

        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium">Transmission</span>
          <select
            className="border border-line rounded-md px-3 py-2 bg-surface"
            value={prefs.transmission_preference}
            onChange={(e) => set("transmission_preference", e.target.value)}
          >
            <option value="">No preference</option>
            <option value="Manual">Manual</option>
            <option value="Automatic">Automatic</option>
          </select>
        </label>

        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium">Parking constraint</span>
          <select
            className="border border-line rounded-md px-3 py-2 bg-surface"
            value={prefs.parking_constraint}
            onChange={(e) => set("parking_constraint", e.target.value)}
          >
            <option value="tight">Tight (narrow street/society)</option>
            <option value="normal">Normal</option>
            <option value="spacious">Spacious</option>
          </select>
        </label>

        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium">Safety importance (1-5)</span>
          <input
            type="range"
            min={1}
            max={5}
            value={prefs.safety_importance}
            onChange={(e) => set("safety_importance", e.target.value)}
          />
        </label>

        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium">Service network importance (1-5)</span>
          <input
            type="range"
            min={1}
            max={5}
            value={prefs.service_availability_importance}
            onChange={(e) => set("service_availability_importance", e.target.value)}
          />
        </label>

        <div className="flex gap-4 sm:col-span-2">
          <label className="flex items-center gap-2 text-sm">
            <input type="checkbox" checked={prefs.elderly_passengers} onChange={(e) => set("elderly_passengers", e.target.checked)} />
            Elderly passengers
          </label>
          <label className="flex items-center gap-2 text-sm">
            <input type="checkbox" checked={prefs.beginner_driver} onChange={(e) => set("beginner_driver", e.target.checked)} />
            Beginner driver
          </label>
        </div>

        <div className="sm:col-span-2">
          <button
            type="submit"
            disabled={status === "loading"}
            className="bg-primary text-white font-medium px-5 py-2.5 rounded-md hover:bg-primary-soft transition-colors disabled:opacity-60"
          >
            {status === "loading" ? "Scoring vehicles…" : "Get recommendations"}
          </button>
        </div>
      </form>

      {status === "error" && (
        <div className="mb-6 text-sm text-danger bg-caution-soft border border-caution rounded-md px-4 py-3">{errorMsg}</div>
      )}

      {results && results.length === 0 && (
        <EmptyState
          title="No matches yet"
          description="Nothing in the catalog fits this budget and these filters. Add manufacturers, cars, and variants from the Catalog page, or widen your filters."
          action={
            <Link to="/catalog" className="text-primary font-medium hover:underline text-sm">
              Go to Catalog &rarr;
            </Link>
          }
        />
      )}

      {results && results.length > 0 && (
        <div className="grid gap-4">
          {results.map((rec, i) => (
            <RecommendationCard key={rec.variant.id} rec={rec} rank={i} />
          ))}
        </div>
      )}
    </div>
  );
}
