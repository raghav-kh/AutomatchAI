import HeroSection from "../components/landing/HeroSection";
import DatasetMetricsBar from "../components/landing/DatasetMetricsBar";
import FeaturedSpotlights from "../components/landing/FeaturedSpotlights";
import FeatureGrid from "../components/landing/FeatureGrid";
import LandingCTA from "../components/landing/LandingCTA";

export default function LandingPage() {
  return (
    <div className="space-y-4 animate-fade-in">
      <HeroSection />
      <DatasetMetricsBar />
      <FeaturedSpotlights />
      <FeatureGrid />
      <LandingCTA />
    </div>
  );
}
