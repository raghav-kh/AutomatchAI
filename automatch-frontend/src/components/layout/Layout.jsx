import { useState } from "react";
import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";
import Footer from "./Footer";
import LoginForm from "../LoginForm";
import { X, ShieldCheck } from "lucide-react";

export default function Layout() {
  const [authModalOpen, setAuthModalOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[var(--color-bg)] text-[var(--color-text-main)] font-body flex flex-col selection:bg-indigo-500/30 selection:text-indigo-200">
      <Navbar onOpenAuth={() => setAuthModalOpen(true)} />
      
      <main className="flex-1">
        <Outlet />
      </main>

      <Footer />

      {/* Admin Auth Modal */}
      {authModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fade-in" role="dialog" aria-modal="true" aria-labelledby="auth-modal-title">
          <div className="solid-card rounded-2xl p-6 max-w-md w-full relative border border-[var(--color-line-bright)] shadow-[var(--shadow-glow-primary)]">
            <button
              onClick={() => setAuthModalOpen(false)}
              className="absolute top-4 right-4 p-1 rounded-lg text-[var(--color-text-muted)] hover:text-white hover:bg-white/5"
              aria-label="Close authentication modal"
            >
              <X className="w-5 h-5" />
            </button>
            
            <div className="flex items-center gap-2 mb-4">
              <ShieldCheck className="w-5 h-5 text-indigo-400" />
              <h3 id="auth-modal-title" className="font-display font-bold text-lg text-white">
                Admin Authentication
              </h3>
            </div>
            <p className="text-xs text-[var(--color-text-muted)] mb-5 leading-relaxed">
              Sign in to manage catalog items, add vehicle variants, or trigger live data scraper pipelines.
            </p>

            <LoginForm onSuccess={() => setAuthModalOpen(false)} />
          </div>
        </div>
      )}
    </div>
  );
}
