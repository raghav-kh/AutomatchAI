import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { compareVariants } from "../api/client";
import VariantSelector from "../components/compare/VariantSelector";
import CompareMatrix from "../components/compare/CompareMatrix";
import SectionHeading from "../components/ui/SectionHeading";
import EmptyState from "../components/ui/EmptyState";
import ErrorAlert from "../components/ui/ErrorAlert";
import Badge from "../components/ui/Badge";
import { ArrowRightLeft, Scale } from "lucide-react";

export default function ComparePage() {
  const location = useLocation();
  const [picked, setPicked] = useState([]);
  const [rows, setRows] = useState(null);
  const [status, setStatus] = useState("idle"); // idle | loading | error
  const [errorMsg, setErrorMsg] = useState("");

  // Handle incoming variant state from Recommendation Card navigation
  useEffect(() => {
    if (location.state?.initialVariant) {
      const v = location.state.initialVariant;
      setPicked((prev) => {
        if (prev.some((p) => p.variant_id === v.id)) return prev;
        return [...prev, { variant_id: v.id, car_model: v.car_model || v.model, variant_name: v.variant_name }];
      });
    }
  }, [location.state]);

  async function runCompare() {
    if (picked.length < 2) return;
    setStatus("loading");
    setErrorMsg("");
    try {
      const data = await compareVariants(picked.map((p) => p.variant_id));
      setRows(data);
      setStatus("idle");
    } catch (err) {
      setStatus("error");
      setErrorMsg("Comparison query failed. Please verify at least 2 valid variants are selected.");
    }
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 md:py-12 space-y-8">
      <SectionHeading
        badge={<Badge variant="primary" icon={ArrowRightLeft}>Side-by-Side Matrix</Badge>}
        title="Smart Multi-Car Comparison"
        subtitle="Compare key technical specifications, safety ratings, boot space, and AI recommendation scores side-by-side."
      />

      <VariantSelector
        picked={picked}
        setPicked={setPicked}
        onCompare={runCompare}
        loading={status === "loading"}
      />

      {status === "error" && (
        <ErrorAlert
          title="Comparison Failed"
          message={errorMsg}
          onRetry={runCompare}
        />
      )}

      {/* Empty State: Less than 2 picked */}
      {!rows && picked.length < 2 && (
        <EmptyState
          icon={Scale}
          title="Select 2 or More Variants to Compare"
          description="Choose car models and specific variants above to initiate a detailed multi-vehicle spec matrix comparison."
        />
      )}

      {/* Comparison Matrix View */}
      {rows && (
        <div className="space-y-4 animate-fade-in pt-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-bold font-display text-white">
              Comparison Results ({rows.length} Vehicles)
            </h3>
            <span className="text-xs text-emerald-400 font-mono flex items-center gap-1">
              • Winning specs highlighted
            </span>
          </div>

          <CompareMatrix rows={rows} />
        </div>
      )}
    </div>
  );
}
