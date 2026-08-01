# AutoMatch AI — Frontend

React + Tailwind + React Router + Axios, per the SRS's tech stack (Section 10).

Talks to the `automatch-ai` backend (Phases 1-4 + admin auth + real
ingestion pipeline). Nothing here calls Groq or any AI service directly --
it's a thin client over the backend's REST API.

## Design direction

Built around an "instrument cluster" concept rather than a generic
dealership-site look: fog-grey background, ink text, a dashboard-indigo
primary and signal-green accent, numbers set in monospace (IBM Plex Mono)
like a digital readout. The signature element is `ConfidenceGauge` -- an SVG
arc gauge styled like a speedometer, used everywhere a confidence/quality
percentage appears, so the "Recommendation Confidence" the SRS calls for
(Section 4.4) has a real visual instead of a plain number.

## Auth

The backend requires an admin token for catalog writes (see the backend's
README). This app now handles that:

- **`AuthContext`** (`src/context/AuthContext.jsx`) tracks the current
  admin user app-wide and exposes `login()`/`logout()`.
- **`LoginForm`** (`src/components/LoginForm.jsx`) handles both sign-in and
  first-time admin registration (gated by the backend's `ADMIN_SETUP_KEY`
  -- there's no public sign-up).
- The JWT is stored in `localStorage` and attached to every request via an
  axios default header; a response interceptor clears it automatically if
  the backend ever returns 401 (expired/invalid token), so the UI drops
  back to a logged-out state instead of failing silently forever.
- **Browsing stays open to everyone.** Only the Catalog page's add/edit/
  delete actions require sign-in -- matching the backend's public-read,
  admin-write split exactly. If you're not signed in, the Catalog page
  shows the `LoginForm` inline above the (still fully visible) tables.

## Pages

- **`/` -- Recommend**: the preference form (SRS 4.1) -> ranked results with
  score breakdown, confidence gauge, reasons/trade-offs, and explanation
  (SRS 4.3/4.4). No sign-in required.
- **`/compare`**: pick 2-10 variants via car/variant dropdowns, see them
  side by side (SRS 4.6). No sign-in required.
- **`/catalog`**: browse manufacturers/cars/variants freely; sign in to
  add, edit, or delete. Since real scrapers only cover a couple of
  manufacturers so far, this is how you populate a demo-ready catalog by
  hand.
- **`/variants/:id`**: ownership cost calculator (SRS 4.5) and "you may
  also consider" alternatives (SRS 4.7) for a specific variant. No sign-in
  required.

## Running

```bash
npm install
cp .env.example .env   # set VITE_API_BASE_URL if the backend isn't on :8000
npm run dev
```

Requires the backend running (see `automatch-ai/README.md`) and reachable
at `VITE_API_BASE_URL` -- the backend's default CORS config already allows
`http://localhost:5173`.

**First-time setup**: go to `/catalog`, use the "First time here? Set up
an admin account" link in the login form, and enter the backend's
`ADMIN_SETUP_KEY` (from its `.env`, default `dev-only-insecure-setup-key-change-me`
unless changed). After that, just sign in.

```bash
npm run build      # production build to dist/
npm run preview    # serve the production build locally
```

## Notes

- If `/recommendations` or `/compare` come back empty, it's almost always
  because the catalog has no cars/variants yet -- sign in and add some via
  `/catalog`, or run the ingestion pipeline (see backend README) for the
  manufacturers that already have a real scraper/API client assigned.
- `EmptyState` treats an empty catalog as an actionable moment (links
  straight to `/catalog`) rather than a dead end, per design guidance.
