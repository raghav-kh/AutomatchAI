import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { getRecommendations } from "../api/client";
import RecommendForm from "../components/recommendation/RecommendForm";
import RecommendationCard from "../components/recommendation/RecommendationCard";
import SectionHeading from "../components/ui/SectionHeading";
import { CardSkeleton } from "../components/ui/Skeleton";
import EmptyState from "../components/ui/EmptyState";
import ErrorAlert from "../components/ui/ErrorAlert";
import Badge from "../components/ui/Badge";
import { Sparkles } from "lucide-react";

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
  const navigate = useNavigate();
  const [prefs, setPrefs] = useState(DEFAULT_PREFS);
  const [results, setResults] = useState(null);
  const [status, setStatus] = useState("idle"); // idle | loading | error
  const [errorMsg, setErrorMsg] = useState("");

  async function fetchRecommendations() {
    setStatus("loading");
    setErrorMsg("");
    try {
      const data = await getRecommendations(cleanPayload(prefs), 10);
      setResults(data);
      setStatus("idle");
    } catch (err) {
      setStatus("error");
      setErrorMsg(
        err?.response?.data?.detail
          ? typeof err.response.data.detail === "string"
            ? err.response.data.detail
            : JSON.stringify(err.response.data.detail)
          : "Unable to connect to the AutoMatch API. Ensure backend service is running on http://localhost:8000."
      );
    }
  }

  function handleSubmit(e) {
    e.preventDefault();
    fetchRecommendations();
  }

  function handleAddToCompare(variant) {
    navigate("/compare", { state: { initialVariant: variant } });
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 md:py-12 space-y-10">
      <SectionHeading
        badge={<Badge variant="cyan" icon={Sparkles}>Decision Support Engine</Badge>}
        title="Find Cars Matched to Your Real Life"
        subtitle="Instead of manually sifting through endless spec tables, state your budget and preferences to receive weighted 11-factor recommendations."
      />

      <RecommendForm
        prefs={prefs}
        setPrefs={setPrefs}
        onSubmit={handleSubmit}
        loading={status === "loading"}
      />

      {/* Error UX State */}
      {status === "error" && (
        <ErrorAlert
          title="Recommendation Request Failed"
          message={errorMsg}
          onRetry={fetchRecommendations}
        />
      )}

      {/* Loading UX State */}
      {status === "loading" && (
        <div className="space-y-4 pt-4">
          <CardSkeleton />
          <CardSkeleton />
          <CardSkeleton />
        </div>
      )}

      {/* Empty UX State */}
      {results && results.length === 0 && status !== "loading" && (
        <EmptyState
          title="No Vehicles Matched Your Criteria"
          description="None of the vehicles in our current catalog fit your budget or filters. Try adjusting your budget slider or relaxing body/fuel constraints."
        />
      )}

      {/* Results View */}
      {results && results.length > 0 && status !== "loading" && (
        <div className="space-y-6 pt-4 animate-fade-in">
          <div className="flex items-center justify-between border-b border-[var(--color-line)] pb-3">
            <h3 className="text-lg font-bold font-display text-white">
              Top Ranked Vehicles ({results.length})
            </h3>
            <span className="text-xs text-[var(--color-text-dim)] font-mono">
              Scored via 11 weighted algorithms
            </span>
          </div>

          <div className="grid gap-6">
            {results.map((rec, i) => (
              <RecommendationCard
                key={rec.variant.id}
                rec={rec}
                rank={i}
                onAddToCompare={handleAddToCompare}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
