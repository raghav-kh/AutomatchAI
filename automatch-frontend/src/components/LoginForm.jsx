import { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { register as apiRegister } from "../api/client";

export default function LoginForm({ onSuccess }) {
  const { login } = useAuth();
  const [mode, setMode] = useState("login"); // "login" | "register"
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [setupKey, setSetupKey] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function handleLogin(e) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      await login(username, password);
      onSuccess?.();
    } catch {
      setError("Incorrect username or password.");
    } finally {
      setBusy(false);
    }
  }

  async function handleRegister(e) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      await apiRegister(username, password, setupKey);
      await login(username, password);
      onSuccess?.();
    } catch (err) {
      setError(err?.response?.data?.detail ?? "Registration failed — check your setup key.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="bg-surface border border-line rounded-lg p-5 max-w-sm">
      <h2 className="font-display font-semibold text-lg mb-1">{mode === "login" ? "Admin sign in" : "First-time admin setup"}</h2>
      <p className="text-ink-soft text-sm mb-4">
        {mode === "login" ? "Catalog edits require an admin account." : "Requires the ADMIN_SETUP_KEY set on the backend."}
      </p>

      <form onSubmit={mode === "login" ? handleLogin : handleRegister} className="flex flex-col gap-3">
        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium">Username</span>
          <input required className="border border-line rounded-md px-3 py-2" value={username} onChange={(e) => setUsername(e.target.value)} />
        </label>
        <label className="flex flex-col gap-1 text-sm">
          <span className="font-medium">Password</span>
          <input
            type="password"
            required
            minLength={mode === "register" ? 8 : undefined}
            className="border border-line rounded-md px-3 py-2"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        {mode === "register" && (
          <label className="flex flex-col gap-1 text-sm">
            <span className="font-medium">Setup key</span>
            <input
              required
              type="password"
              className="border border-line rounded-md px-3 py-2"
              value={setupKey}
              onChange={(e) => setSetupKey(e.target.value)}
            />
          </label>
        )}

        {error && <div className="text-sm text-danger bg-caution-soft border border-caution rounded-md px-3 py-2">{error}</div>}

        <button
          type="submit"
          disabled={busy}
          className="bg-primary text-white font-medium px-4 py-2 rounded-md hover:bg-primary-soft disabled:opacity-60"
        >
          {busy ? "Please wait…" : mode === "login" ? "Sign in" : "Create admin account"}
        </button>
      </form>

      <button
        type="button"
        onClick={() => {
          setMode(mode === "login" ? "register" : "login");
          setError("");
        }}
        className="text-xs text-primary hover:underline mt-3"
      >
        {mode === "login" ? "First time here? Set up an admin account" : "Already have an account? Sign in"}
      </button>
    </div>
  );
}
