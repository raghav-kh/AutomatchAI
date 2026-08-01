import { useState } from "react";
import { Sparkles, Sliders, IndianRupee, Users, Car, Fuel, Shield, AlertCircle } from "lucide-react";
import Button from "../ui/Button";
import SolidCard from "../ui/SolidCard";

const PRESETS = [
  {
    name: "₹10L Urban SUV",
    values: {
      budget: 1000000,
      family_members: 4,
      daily_running_km: 25,
      highway_usage: "occasional",
      body_type_preference: "SUV",
      fuel_preference: "",
      transmission_preference: "",
      safety_importance: 4,
      service_availability_importance: 3,
      parking_constraint: "normal",
      elderly_passengers: false,
      beginner_driver: false,
    },
  },
  {
    name: "Family 7-Seater",
    values: {
      budget: 1800000,
      family_members: 7,
      daily_running_km: 30,
      highway_usage: "frequent",
      body_type_preference: "MPV",
      fuel_preference: "Diesel",
      transmission_preference: "Automatic",
      safety_importance: 5,
      service_availability_importance: 4,
      parking_constraint: "spacious",
      elderly_passengers: true,
      beginner_driver: false,
    },
  },
  {
    name: "City EV Commuter",
    values: {
      budget: 1200000,
      family_members: 3,
      daily_running_km: 45,
      highway_usage: "rare",
      body_type_preference: "Hatchback",
      fuel_preference: "Electric",
      transmission_preference: "Automatic",
      safety_importance: 4,
      service_availability_importance: 3,
      parking_constraint: "tight",
      elderly_passengers: false,
      beginner_driver: true,
    },
  },
];

export default function RecommendForm({ prefs, setPrefs, onSubmit, loading }) {
  function update(field, value) {
    setPrefs((prev) => ({ ...prev, [field]: value }));
  }

  function applyPreset(presetValues) {
    setPrefs(presetValues);
  }

  return (
    <form onSubmit={onSubmit} className="space-y-6">
      {/* Presets Bar */}
      <div className="flex flex-wrap items-center gap-2">
        <span className="text-xs font-semibold text-[var(--color-text-muted)] uppercase tracking-wider flex items-center gap-1">
          <Sparkles className="w-3.5 h-3.5 text-cyan-400" /> Presets:
        </span>
        {PRESETS.map((preset) => (
          <button
            key={preset.name}
            type="button"
            onClick={() => applyPreset(preset.values)}
            className="text-xs bg-[var(--color-surface-subtle)] text-[var(--color-text-muted)] hover:text-white hover:bg-[var(--color-primary-soft)] hover:border-[var(--color-primary)] border border-[var(--color-line)] px-3 py-1.5 rounded-full transition-all button-press"
          >
            {preset.name}
          </button>
        ))}
      </div>

      <SolidCard className="space-y-6 border border-[var(--color-line-bright)]">
        {/* Fieldset 1: Budget & Vehicle Type */}
        <div>
          <h3 className="text-sm font-semibold font-display text-white uppercase tracking-wider mb-4 flex items-center gap-2">
            <IndianRupee className="w-4 h-4 text-cyan-400" /> 1. Budget & Vehicle Preference
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <label className="flex flex-col gap-1.5">
              <span className="text-xs font-medium text-[var(--color-text-muted)]">Budget (ex-showroom ₹)</span>
              <div className="relative">
                <input
                  type="number"
                  required
                  min={100000}
                  step={50000}
                  value={prefs.budget}
                  onChange={(e) => update("budget", e.target.value)}
                  className="w-full bg-[var(--color-surface-subtle)] border border-[var(--color-line)] rounded-xl px-3.5 py-2.5 text-sm font-mono text-white focus:border-[var(--color-primary)]"
                />
                <div className="text-[10px] font-mono text-cyan-400 mt-1">
                  ₹{(Number(prefs.budget) / 100000).toFixed(1)} Lakh
                </div>
              </div>
            </label>

            <label className="flex flex-col gap-1.5">
              <span className="text-xs font-medium text-[var(--color-text-muted)]">Body Type</span>
              <select
                value={prefs.body_type_preference}
                onChange={(e) => update("body_type_preference", e.target.value)}
                className="w-full bg-[var(--color-surface-subtle)] border border-[var(--color-line)] rounded-xl px-3.5 py-2.5 text-sm text-white focus:border-[var(--color-primary)]"
              >
                <option value="">Any Body Type</option>
                <option value="Hatchback">Hatchback</option>
                <option value="Sedan">Sedan</option>
                <option value="SUV">SUV</option>
                <option value="MPV">MPV</option>
              </select>
            </label>

            <label className="flex flex-col gap-1.5">
              <span className="text-xs font-medium text-[var(--color-text-muted)] font-sans">Fuel Type</span>
              <select
                value={prefs.fuel_preference}
                onChange={(e) => update("fuel_preference", e.target.value)}
                className="w-full bg-[var(--color-surface-subtle)] border border-[var(--color-line)] rounded-xl px-3.5 py-2.5 text-sm text-white focus:border-[var(--color-primary)]"
              >
                <option value="">Any Fuel Type</option>
                <option value="Petrol">Petrol</option>
                <option value="Diesel">Diesel</option>
                <option value="CNG">CNG</option>
                <option value="Electric">Electric</option>
                <option value="Hybrid">Hybrid</option>
              </select>
            </label>
          </div>
        </div>

        <hr className="border-[var(--color-line)]" />

        {/* Fieldset 2: Driving Habits & Family */}
        <div>
          <h3 className="text-sm font-semibold font-display text-white uppercase tracking-wider mb-4 flex items-center gap-2">
            <Car className="w-4 h-4 text-indigo-400" /> 2. Usage & Driving Profile
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <label className="flex flex-col gap-1.5">
              <span className="text-xs font-medium text-[var(--color-text-muted)]">Family Size</span>
              <input
                type="number"
                min={1}
                max={10}
                placeholder="e.g. 4"
                value={prefs.family_members}
                onChange={(e) => update("family_members", e.target.value)}
                className="w-full bg-[var(--color-surface-subtle)] border border-[var(--color-line)] rounded-xl px-3.5 py-2.5 text-sm text-white focus:border-[var(--color-primary)]"
              />
            </label>

            <label className="flex flex-col gap-1.5">
              <span className="text-xs font-medium text-[var(--color-text-muted)]">Daily Running (km)</span>
              <input
                type="number"
                min={0}
                placeholder="e.g. 25"
                value={prefs.daily_running_km}
                onChange={(e) => update("daily_running_km", e.target.value)}
                className="w-full bg-[var(--color-surface-subtle)] border border-[var(--color-line)] rounded-xl px-3.5 py-2.5 text-sm text-white focus:border-[var(--color-primary)]"
              />
            </label>

            <label className="flex flex-col gap-1.5">
              <span className="text-xs font-medium text-[var(--color-text-muted)]">Highway Usage</span>
              <select
                value={prefs.highway_usage}
                onChange={(e) => update("highway_usage", e.target.value)}
                className="w-full bg-[var(--color-surface-subtle)] border border-[var(--color-line)] rounded-xl px-3.5 py-2.5 text-sm text-white focus:border-[var(--color-primary)]"
              >
                <option value="rare">Rare (City commute)</option>
                <option value="occasional">Occasional (Weekend trips)</option>
                <option value="frequent">Frequent (Intercity highway)</option>
              </select>
            </label>

            <label className="flex flex-col gap-1.5">
              <span className="text-xs font-medium text-[var(--color-text-muted)]">Transmission</span>
              <select
                value={prefs.transmission_preference}
                onChange={(e) => update("transmission_preference", e.target.value)}
                className="w-full bg-[var(--color-surface-subtle)] border border-[var(--color-line)] rounded-xl px-3.5 py-2.5 text-sm text-white focus:border-[var(--color-primary)]"
              >
                <option value="">No Preference</option>
                <option value="Manual">Manual</option>
                <option value="Automatic">Automatic</option>
              </select>
            </label>
          </div>
        </div>

        <hr className="border-[var(--color-line)]" />

        {/* Fieldset 3: Safety & Network Importance */}
        <div>
          <h3 className="text-sm font-semibold font-display text-white uppercase tracking-wider mb-4 flex items-center gap-2">
            <Shield className="w-4 h-4 text-emerald-400" /> 3. Priorities & Parking
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-1.5">
              <div className="flex justify-between items-center text-xs">
                <span className="font-medium text-[var(--color-text-muted)]">Safety Importance</span>
                <span className="font-mono text-emerald-400 font-bold">{prefs.safety_importance} / 5</span>
              </div>
              <input
                type="range"
                min={1}
                max={5}
                value={prefs.safety_importance}
                onChange={(e) => update("safety_importance", e.target.value)}
                className="w-full accent-[var(--color-success)] cursor-pointer"
              />
            </div>

            <div className="space-y-1.5">
              <div className="flex justify-between items-center text-xs">
                <span className="font-medium text-[var(--color-text-muted)]">Service Network Importance</span>
                <span className="font-mono text-indigo-400 font-bold">{prefs.service_availability_importance} / 5</span>
              </div>
              <input
                type="range"
                min={1}
                max={5}
                value={prefs.service_availability_importance}
                onChange={(e) => update("service_availability_importance", e.target.value)}
                className="w-full accent-[var(--color-primary)] cursor-pointer"
              />
            </div>

            <label className="flex flex-col gap-1.5">
              <span className="text-xs font-medium text-[var(--color-text-muted)]">Parking Environment</span>
              <select
                value={prefs.parking_constraint}
                onChange={(e) => update("parking_constraint", e.target.value)}
                className="w-full bg-[var(--color-surface-subtle)] border border-[var(--color-line)] rounded-xl px-3.5 py-2.5 text-sm text-white focus:border-[var(--color-primary)]"
              >
                <option value="tight">Tight (Narrow street / stack parking)</option>
                <option value="normal">Normal Parking</option>
                <option value="spacious">Spacious Parking</option>
              </select>
            </label>
          </div>

          <div className="flex flex-wrap items-center gap-6 mt-4 pt-2">
            <label className="inline-flex items-center gap-2 cursor-pointer text-xs font-medium text-white">
              <input
                type="checkbox"
                checked={prefs.elderly_passengers}
                onChange={(e) => update("elderly_passengers", e.target.checked)}
                className="w-4 h-4 rounded border-[var(--color-line)] text-indigo-500 focus:ring-indigo-400"
              />
              Elderly passengers (requires easy ingress/egress)
            </label>
            <label className="inline-flex items-center gap-2 cursor-pointer text-xs font-medium text-white">
              <input
                type="checkbox"
                checked={prefs.beginner_driver}
                onChange={(e) => update("beginner_driver", e.target.checked)}
                className="w-4 h-4 rounded border-[var(--color-line)] text-indigo-500 focus:ring-indigo-400"
              />
              Beginner driver (prioritize compact dimensions & visibility)
            </label>
          </div>
        </div>

        {/* Submit CTA */}
        <div className="pt-2">
          <Button type="submit" variant="cyan" size="lg" loading={loading} icon={Sparkles} className="w-full sm:w-auto">
            {loading ? "Calculating 11-Factor Match Scores…" : "Calculate AI Car Recommendations"}
          </Button>
        </div>
      </SolidCard>
    </form>
  );
}
