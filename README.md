# AutoMatch AI

**AI-powered car recommendation & decision-support system for the Indian market.**

Most car-shopping platforms assume you already know which cars to compare.
AutoMatch AI works backwards from what buyers actually know — budget,
family size, commute, driving habits — and finds the right car, including
ones you'd never have thought to search for (a ₹10L SUV budget shouldn't
only surface Tata and Hyundai; it should surface the Citroën Basalt too).

Every recommendation comes with a score breakdown, a confidence rating,
plain-language reasons and trade-offs, and — if configured — an
LLM-generated explanation. Beyond recommendations, it also handles
5-year ownership cost estimates, side-by-side comparisons, and
"you may also consider..." alternatives.

Full original spec: this project was built against a Software Requirements
Specification covering 13 sections and 8 major feature areas — most of
what's below maps directly to a numbered SRS section, called out inline.

---

## Try it in 2 minutes

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
python -m scripts.seed_demo_catalog   # 7 manufacturers, 12 cars, 13 variants, fully specced
uvicorn app.main:app --reload
```

```bash
# In a second terminal — Frontend
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open `http://localhost:5173`. With the demo catalog seeded, the homepage's
default form recreates the SRS's own worked example immediately: a ₹10L
SUV budget surfaces both the Tata Nexon **and** the Citroën Basalt —
exactly the "buyers miss cars they don't know exist" problem this project
was built to solve.

No `GROQ_API_KEY`? No problem — explanations fall back to a clear
template automatically. Nothing in the demo requires an LLM key, a cloud
database, or any external account.

---

## What's actually working

This isn't a mockup — every item below is implemented, tested, and
verified against a live server, not just described.

| Area | What it does | SRS ref |
|---|---|---|
| **Recommendation engine** | 11-factor weighted scoring (budget fit, safety, family fit, city/highway comfort, maintenance, resale, service network, fuel/transmission match, parking fit) — weights shift based on stated preferences, not fixed | §4.1–4.4, §9 |
| **Confidence scoring** | Separate from match score — blends match quality, data completeness, and manufacturer data-source trust | §4.4 |
| **Explainable AI** | Plain-language reasons/trade-offs from the score breakdown; LLM explanation (Groq) with automatic template fallback and a **consistency guard** that rejects any LLM text contradicting the actual score | §4.3–4.4 |
| **Ownership cost calculator** | Purchase price, insurance, fuel, maintenance, road tax, expected resale, 5-year net cost — every assumption returned explicitly, nothing hidden | §4.5 |
| **Smart comparisons** | Side-by-side comparison across performance, safety, maintenance, boot space, and a context-free AI recommendation score | §4.6 |
| **Alternative recommendations** | "You may also consider X because..." — verified live with the SRS's own example (XUV 3XO → Honda Elevate) | §4.7 |
| **Data ingestion pipeline** | Manufacturer classification (API vs. scraper), a real working scraper against Tata Motors' official site, a real API client against a live government vehicle API, full audit logging | §6, §9 |
| **Admin auth** | JWT-based, bcrypt-hashed, gated registration — protects every catalog write while keeping all reads (recommendations, comparisons, browsing) public | — |
| **Catalog management UI** | Full CRUD for manufacturers/cars/variants with nested specs & AI attributes, gated behind sign-in | — |

---

## Architecture

```
                    ┌─────────────────┐
                    │   React + Vite   │   frontend/
                    │  (Tailwind, RR)  │
                    └────────┬─────────┘
                             │ REST (axios)
                    ┌────────▼─────────┐
                    │     FastAPI      │   backend/app/
                    │  (Pydantic v2)   │
                    └────────┬─────────┘
              ┌──────────────┼──────────────┐
      ┌───────▼──────┐ ┌─────▼──────┐ ┌─────▼──────┐
      │ Recommendation│ │  Pipeline  │ │    Auth    │
      │    Engine     │ │ (scrapers, │ │ (JWT/bcrypt)│
      │ (scoring, cost,│ │ API clients,│ └────────────┘
      │  comparisons)  │ │ dispatcher)│
      └───────┬───────┘ └─────┬──────┘
              └────────┬───────┘
                ┌───────▼────────┐
                │  SQLAlchemy 2.0 │
                │ (SQLite / Supabase)│
                └─────────────────┘
```

**Backend**: FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2, psycopg3
(Postgres/Supabase-ready), PyJWT + bcrypt, pytest.
**Frontend**: React 19, Vite, Tailwind v4, React Router, Axios.
**AI**: Groq (Llama 3.3) for explanations — optional, degrades gracefully
without a key.

---

## Project structure

```
automatch-ai/
├── backend/
│   ├── app/
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic request/response models
│   │   ├── crud/            # DB access layer
│   │   ├── api/routes/      # FastAPI routers
│   │   ├── recommendation/  # scoring, confidence, ownership cost,
│   │   │                    # comparison, alternatives, explainer
│   │   ├── pipeline/        # scrapers, API clients, dispatcher
│   │   └── core/            # config, database, security
│   ├── alembic/              # migrations
│   ├── scripts/               # seed_demo_catalog.py, seed_manufacturers.py
│   ├── tests/                 # 101 tests, incl. real captured-data fixtures
│   └── README.md              # full backend documentation
└── frontend/
    ├── src/
    │   ├── pages/            # Recommend, Compare, Catalog, VariantDetail
    │   ├── components/       # ConfidenceGauge, ScoreBar, LoginForm, etc.
    │   ├── context/          # AuthContext
    │   └── api/               # axios client
    └── README.md              # full frontend documentation
```

Each half has its own detailed README — this one is the map; `backend/README.md`
and `frontend/README.md` go deep on how each piece actually works.

---

## Real data, not mock data

Two things in this project are deliberately built against **real, live
sources** rather than hypothetical schemas, because that's where the
actual engineering challenges show up:

- **`backend/app/pipeline/scrapers/tata.py`** — a working scraper against
  `cars.tatamotors.com`'s official pricing pages. Built from an actual
  captured page, tested against it, and honest about what it can't get:
  exact prices are loaded client-side by the manufacturer's own site, so
  every scraped variant reports `price=None` rather than a fabricated
  number — with a documented path (headless browser) to close that gap.
- **`backend/app/pipeline/scrapers/nhtsa_vpic.py`** — a working API client
  against NHTSA's free, public vPIC vehicle database, verified with a live
  fetch. Also upfront about its limits: it's a compliance database, not a
  pricing catalog, and doesn't cover India-only manufacturers.

Both are wired through the same dispatcher, log every run (success or
failure) to an auditable `ScrapeLog` table, and were verified end-to-end
through the real HTTP API — including watching them fail cleanly instead
of crashing when network access was restricted.

## Demo catalog

For the recommendation engine, comparisons, and ownership-cost calculator
to have something real to work with beyond the two live-scraped sources,
`backend/scripts/seed_demo_catalog.py` populates 7 manufacturers, 12 cars,
and 13 fully-specced variants — and it directly recreates the SRS's own
worked examples:

- **₹10L SUV budget** → Tata Nexon and Citroën Basalt both surface
- **Family of 7** → the Mahindra XUV700 (the only 7-seater) wins
- **Short daily commute** → the Nexon EV is correctly scored down
- **Select the XUV 3XO** → alternatives correctly suggest the Honda
  Elevate, with the reasons "Better refinement / Better resale value /
  More reliable, lower maintenance"

## Testing

```bash
cd backend && pytest tests/ -v
```

101 tests: full CRUD coverage, the scoring engine's weight-shifting logic,
the explanation consistency guard (including a case where it correctly
rejects an LLM response contradicting the real score), ownership-cost
math, comparison/alternative logic, end-to-end admin auth (real
registration/login/token flow), and both real scrapers tested against
their actual captured data.

## What's not built yet

Honestly, not everything — this is a working prototype, not a finished
product:

- Real scrapers/API clients for manufacturers beyond Tata Motors and the
  vPIC demo (the pattern is proven; most manufacturers still need their
  own adapter written)
- Live deployment (Supabase-ready, psycopg3, but nothing is hosted yet)
- Pipeline scheduling (classification/ingestion run on-demand, not on a cron)
- Rate limiting
- SRS §11 future enhancements: EMI calculator, dealer locator, live fuel
  price integration, used-car/EV-specific recommendations, multilingual
  support, and more

See `backend/README.md`'s "Still not built" section for the full,
unvarnished list.

## License

No license file included yet — add one (MIT is a common default for a
portfolio project like this) before treating this as open source.