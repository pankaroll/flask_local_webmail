import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql+psycopg2://mailo:mailo@localhost:5433/mailo_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_DOMAIN = os.getenv("MAIL_DOMAIN", "mailo.local")

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False