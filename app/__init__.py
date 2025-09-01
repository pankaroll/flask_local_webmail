from flask import Flask, jsonify
from .core.config import Config
from .db import db
from sqlalchemy import text, inspect


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config.setdefault("SESSION_COOKIE_HTTPONLY", True)
    app.config.setdefault("SESSION_COOKIE_SAMESITE", "Lax")

    db.init_app(app)

    from .auth.routes import bp as auth_bp
    from .messages.routes import bp as messages_bp
    from .db import models  # noqa: F401

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(messages_bp, url_prefix="/messages")

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    @app.get("/health/db")
    def health_db():
        db.session.execute(text("SELECT 1"))
        return {"db": "ok"}, 200

    @app.route("/debug/tables")
    def list_tables():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        return jsonify(tables)

    return app
