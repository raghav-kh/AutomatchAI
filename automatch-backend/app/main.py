import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app import models  # noqa: F401  (ensures all models are registered before create_all)
from app.api.routes import manufacturers, cars, variants, pipeline, recommendations, comparisons, auth

logger = logging.getLogger("automatch")

# Dev convenience: auto-create tables on SQLite. In real Postgres deployments,
# use Alembic migrations instead (see alembic/ directory) and drop this call.
if settings.database_url.startswith("sqlite"):
    Base.metadata.create_all(bind=engine)

if settings.environment != "development" and (
    settings.secret_key == "dev-only-insecure-secret-change-me"
    or settings.admin_setup_key == "dev-only-insecure-setup-key-change-me"
):
    logger.warning(
        "SECURITY WARNING: SECRET_KEY and/or ADMIN_SETUP_KEY are still set to their "
        "insecure development defaults while ENVIRONMENT != 'development'. Set both "
        "via environment variables before exposing this service."
    )

app = FastAPI(
    title=settings.app_name,
    description="AI-powered car recommendation & decision support backend (Phase 1: core data API)",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(manufacturers.router)
app.include_router(cars.router)
app.include_router(variants.router)
app.include_router(pipeline.router)
app.include_router(recommendations.router)
app.include_router(comparisons.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "service": settings.app_name}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
