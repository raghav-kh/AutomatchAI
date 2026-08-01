import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Layout from "./components/Layout";
import RecommendPage from "./pages/RecommendPage";
import ComparePage from "./pages/ComparePage";
import CatalogPage from "./pages/CatalogPage";
import VariantDetailPage from "./pages/VariantDetailPage";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route index element={<RecommendPage />} />
            <Route path="compare" element={<ComparePage />} />
            <Route path="catalog" element={<CatalogPage />} />
            <Route path="variants/:id" element={<VariantDetailPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
