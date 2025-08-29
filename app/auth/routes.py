from flask import Blueprint, request, session, current_app, g
from sqlalchemy import select
import re

from ..db import db
from ..db.models import User
from ..core.security import hash_password, verify_password
from ..core.auth import login_required

bp = Blueprint("auth", __name__)
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

@bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    display_name = (data.get("display_name") or "").strip() or None
    password = data.get("password") or ""

    if not email or not password:
        return {"error": "email and password required"}, 400
    if not EMAIL_RE.match(email):
        return {"error": "invalid email"}, 400

    domain = current_app.config.get("MAIL_DOMAIN", "mailo.local").lower()
    if not email.endswith(f"@{domain}"):
        return {"error": f"email must be in @{domain} domain"}, 400

    exists = db.session.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if exists:
        return {"error": "email already registered"}, 409

    u = User(email=email, display_name=display_name, password_hash=hash_password(password))
    db.session.add(u)
    db.session.commit()
    return {"id": u.id, "email": u.email, "display_name": u.display_name}, 201

@bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return {"error": "email and password required"}, 400

    user = db.session.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if not user or not verify_password(password, user.password_hash):
        return {"error": "invalid credentials"}, 401
    if not user.is_active:
        return {"error": "inactive account"}, 403

    session.clear()
    session["user_id"] = user.id
    return {"message": "logged in", "user": {"id": user.id, "email": user.email, "display_name": user.display_name}}, 200

@bp.post("/logout")
@login_required
def logout():
    session.clear()
    return {"message": "logged out"}, 200

@bp.get("/me")
@login_required
def me():
    u = g.current_user
    return {"id": u.id, "email": u.email, "display_name": u.display_name, "is_active": u.is_active}, 200
