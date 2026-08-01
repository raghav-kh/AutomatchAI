import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Layout from "./components/layout/Layout";
import LandingPage from "./pages/LandingPage";
import RecommendPage from "./pages/RecommendPage";
import ComparePage from "./pages/ComparePage";
import CatalogPage from "./pages/CatalogPage";
import VariantDetailPage from "./pages/VariantDetailPage";
import AboutPage from "./pages/AboutPage";
import PrivacyPage from "./pages/PrivacyPage";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route index element={<LandingPage />} />
            <Route path="recommend" element={<RecommendPage />} />
            <Route path="compare" element={<ComparePage />} />
            <Route path="catalog" element={<CatalogPage />} />
            <Route path="variants/:id" element={<VariantDetailPage />} />
            <Route path="about" element={<AboutPage />} />
            <Route path="privacy" element={<PrivacyPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
