from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central app configuration, loaded from environment variables / .env.

    NOTE: GROQ_API_KEY is defined here now so the AI phase (Phase 2+) can
    just read settings.groq_api_key without touching this file again.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "AutoMatch AI"
    environment: str = "development"

    # SQLite for local dev by default. For Supabase/Postgres, use the
    # psycopg3 dialect: postgresql+psycopg://...
    # Supabase gives you this connection string directly from
    # Project Settings -> Database -> Connection string -> "URI" (choose the
    # "Session pooler" or direct connection; see README for which to use).
    database_url: str = "sqlite:///./automatch.db"

    # Reserved for Phase 2 (AI recommendation + explanation layer)
    groq_api_key: str | None = None
    groq_model: str = "llama-3.3-70b-versatile"

    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # --- Admin auth ---
    # Protects catalog write endpoints and pipeline triggers. This is
    # separate from the SRS's future "user accounts" feature (buyer-facing
    # saved searches etc, not built) -- this is purely "who's allowed to
    # write to the catalog / kick off scraping".
    secret_key: str = "dev-only-insecure-secret-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24h

    # Required to register the first (and any subsequent) admin account.
    # Registration without the correct key is rejected -- there's no
    # public sign-up, this is an internal admin tool.
    admin_setup_key: str = "dev-only-insecure-setup-key-change-me"


settings = Settings()
