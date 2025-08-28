import os

class Config:
    # KLUCZ do podpisywania sesji — na dev może być stały,
    # docelowo wczytaj z ENV (np. przez python-dotenv)
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")

    # Baza – placeholder; później podmienisz na realne DSN do Postgresa
    # SQLALCHEMY_DATABASE_URI = os.getenv(
    #     "DATABASE_URL",
    #     "postgresql+psycopg2://mailo:mailo@localhost:5432/mailo_db"
    # )
    # SQLALCHEMY_TRACK_MODIFICATIONS = False