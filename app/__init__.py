from flask import Flask
from .core.config import Config

def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config.setdefault("SESSION_COOKIE_HTTPONLY", True)
    app.config.setdefault("SESSION_COOKIE_SAMESITE", "Lax")

    from .auth.routes import bp as auth_bp
    from .messages.routes import bp as messages_bp

    app.register_blueprint(auth_bp, url_prefix = "/auth")
    app.register_blueprint(messages_bp, url_prefix = "/messages")

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200
    
    return app
