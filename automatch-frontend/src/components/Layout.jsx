import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const navItems = [
  { to: "/", label: "Recommend", end: true },
  { to: "/compare", label: "Compare" },
  { to: "/catalog", label: "Catalog" },
];

function GaugeMark() {
  return (
    <svg viewBox="0 0 32 32" className="h-8 w-8" aria-hidden="true">
      <circle cx="16" cy="16" r="14" fill="var(--color-ink)" />
      <path
        d="M6 20A10 10 0 0 1 22 11"
        fill="none"
        stroke="var(--color-accent)"
        strokeWidth="3"
        strokeLinecap="round"
      />
      <circle cx="16" cy="16" r="2.5" fill="var(--color-caution)" />
      <line x1="16" y1="16" x2="21" y2="11" stroke="var(--color-caution)" strokeWidth="2" strokeLinecap="round" />
    </svg>
  );
}

export default function Layout() {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen bg-bg text-ink font-body flex flex-col md:flex-row">
      <aside className="md:w-60 shrink-0 border-b md:border-b-0 md:border-r border-line bg-surface flex md:flex-col">
        <div className="flex-1 flex flex-col">
          <div className="p-5 flex items-center gap-3">
            <GaugeMark />
            <div>
              <div className="font-display font-semibold text-lg leading-tight">AutoMatch AI</div>
              <div className="text-xs text-ink-soft leading-tight">decision dashboard</div>
            </div>
          </div>
          <nav className="px-3 pb-4 flex md:flex-col gap-1">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                className={({ isActive }) =>
                  `flex-1 md:flex-none px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive
                      ? "bg-primary text-white"
                      : "text-ink-soft hover:bg-accent-soft hover:text-ink"
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </div>
        <div className="p-4 border-t border-line text-sm">
          {user ? (
            <div className="flex items-center justify-between gap-2">
              <span className="text-ink-soft truncate">
                Signed in as <span className="text-ink font-medium">{user.username}</span>
              </span>
              <button onClick={logout} className="text-primary hover:underline shrink-0">
                Sign out
              </button>
            </div>
          ) : (
            <span className="text-ink-soft">Not signed in</span>
          )}
        </div>
      </aside>
      <main className="flex-1 min-w-0">
        <div className="max-w-5xl mx-auto p-4 md:p-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
