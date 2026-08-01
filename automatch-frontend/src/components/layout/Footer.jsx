import { Link } from "react-router-dom";
import { Car } from "lucide-react";

export default function Footer() {
  return (
    <footer className="border-t border-[var(--color-line)] bg-slate-950/80 text-[var(--color-text-muted)] text-sm py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 pb-10 border-b border-[var(--color-line)]">
          {/* Brand Info */}
          <div className="space-y-3 md:col-span-1">
            <div className="flex items-center gap-2 font-display font-bold text-lg text-white">
              <Car className="w-5 h-5 text-cyan-400" />
              AutoMatch<span className="text-cyan-400">AI</span>
            </div>
            <p className="text-xs text-[var(--color-text-dim)] leading-relaxed">
              AI-powered car recommendation & decision-support system tailored for Indian car buyers. Ranks cars based on your actual budget, daily commute, family size, and ownership cost.
            </p>
          </div>

          {/* Core Modules */}
          <div className="space-y-2">
            <h4 className="font-display text-xs font-semibold text-white uppercase tracking-wider">Features</h4>
            <ul className="space-y-1.5 text-xs">
              <li><Link to="/recommend" className="hover:text-white transition-colors">11-Factor AI Matcher</Link></li>
              <li><Link to="/compare" className="hover:text-white transition-colors">Smart Multi-Car Compare</Link></li>
              <li><Link to="/catalog" className="hover:text-white transition-colors">Vehicle Catalog & Pipelines</Link></li>
            </ul>
          </div>

          {/* Transparency & Governance */}
          <div className="space-y-2">
            <h4 className="font-display text-xs font-semibold text-white uppercase tracking-wider">Transparency</h4>
            <ul className="space-y-1.5 text-xs">
              <li><Link to="/about" className="hover:text-white transition-colors">About Engine & Algorithm</Link></li>
              <li><Link to="/privacy" className="hover:text-white transition-colors">Data Privacy & Neutrality</Link></li>
            </ul>
          </div>

          {/* Engine Specs */}
          <div className="space-y-2">
            <h4 className="font-display text-xs font-semibold text-white uppercase tracking-wider">System Stack</h4>
            <div className="flex flex-wrap gap-1.5 pt-1">
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/5 border border-white/10 text-cyan-300">FastAPI</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/5 border border-white/10 text-indigo-300">React 19</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/5 border border-white/10 text-emerald-300">Groq LLM</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-white/5 border border-white/10 text-amber-300">SQLAlchemy 2.0</span>
            </div>
          </div>
        </div>

        {/* Copyright */}
        <div className="pt-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-[var(--color-text-dim)]">
          <div>&copy; {new Date().getFullYear()} AutoMatch AI. All rights reserved.</div>
          <div className="flex items-center gap-1">
            <span>Built with precision for Indian car buyers</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
