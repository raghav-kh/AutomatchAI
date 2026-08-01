import { useState } from "react";
import { NavLink, Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { Car, Sparkles, ArrowRightLeft, Database, Menu, X, LogIn, LogOut, ShieldCheck } from "lucide-react";
import Button from "../ui/Button";

const NAV_ITEMS = [
  { to: "/", label: "Home", icon: Car, end: true },
  { to: "/recommend", label: "AI Matcher", icon: Sparkles },
  { to: "/compare", label: "Smart Compare", icon: ArrowRightLeft },
  { to: "/catalog", label: "Catalog", icon: Database },
];

export default function Navbar({ onOpenAuth }) {
  const { user, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full glass-panel border-b border-[var(--color-line)]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-3 group focus:outline-none">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-cyan-400 p-0.5 shadow-[var(--shadow-glow-primary)] transition-transform group-hover:scale-105">
            <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <Car className="w-5 h-5 text-cyan-400" aria-hidden="true" />
            </div>
          </div>
          <div>
            <div className="font-display font-bold text-lg leading-none tracking-tight text-white flex items-center gap-1.5">
              AutoMatch<span className="text-cyan-400">AI</span>
            </div>
            <div className="text-[10px] font-mono text-[var(--color-text-dim)] uppercase tracking-wider">
              Car Match Engine
            </div>
          </div>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center gap-1 bg-[var(--color-surface-subtle)]/60 p-1.5 rounded-xl border border-[var(--color-line)]">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                className={({ isActive }) =>
                  `flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                    isActive
                      ? "bg-[var(--color-primary)] text-white shadow-sm"
                      : "text-[var(--color-text-muted)] hover:text-white hover:bg-white/5"
                  }`
                }
              >
                <Icon className="w-3.5 h-3.5" aria-hidden="true" />
                {item.label}
              </NavLink>
            );
          })}
        </nav>

        {/* User Auth Controls */}
        <div className="hidden md:flex items-center gap-3">
          {user ? (
            <div className="flex items-center gap-3 pl-3 border-l border-[var(--color-line)]">
              <div className="flex items-center gap-1.5 text-xs text-[var(--color-text-muted)]">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                <span>Admin: <strong className="text-white">{user.username}</strong></span>
              </div>
              <Button variant="ghost" size="sm" onClick={logout} icon={LogOut}>
                Sign out
              </Button>
            </div>
          ) : (
            <Button variant="secondary" size="sm" onClick={onOpenAuth} icon={LogIn}>
              Admin Access
            </Button>
          )}
        </div>

        {/* Mobile Hamburger Toggle */}
        <button
          type="button"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="md:hidden p-2 rounded-lg text-[var(--color-text-muted)] hover:text-white hover:bg-white/5 focus:outline-none"
          aria-expanded={mobileMenuOpen}
          aria-label="Toggle navigation menu"
        >
          {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {/* Mobile Drawer Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden glass-panel border-t border-[var(--color-line)] px-4 pt-3 pb-6 space-y-2 animate-fade-in">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                onClick={() => setMobileMenuOpen(false)}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-colors ${
                    isActive
                      ? "bg-[var(--color-primary)] text-white"
                      : "text-[var(--color-text-muted)] hover:bg-white/5 hover:text-white"
                  }`
                }
              >
                <Icon className="w-4 h-4" />
                {item.label}
              </NavLink>
            );
          })}
          <div className="pt-3 border-t border-[var(--color-line)]">
            {user ? (
              <div className="flex items-center justify-between px-2">
                <span className="text-xs text-[var(--color-text-muted)]">
                  Signed in as <strong className="text-white">{user.username}</strong>
                </span>
                <Button variant="ghost" size="sm" onClick={logout}>
                  Sign out
                </Button>
              </div>
            ) : (
              <Button variant="secondary" size="sm" className="w-full" onClick={() => { setMobileMenuOpen(false); onOpenAuth(); }}>
                Admin Sign In
              </Button>
            )}
          </div>
        </div>
      )}
    </header>
  );
}
