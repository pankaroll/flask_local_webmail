from functools import wraps
from flask import session, g
from ..db import db

def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        uid = session.get("user_id")
        if not uid:
            return {"error": "unauthorized"}, 401
        from ..db.models import User
        user = db.session.get(User, uid)
        if not user or not user.is_active:
            session.clear()
            return {"error": "unauthorized"}, 401
        g.current_user = user
        return fn(*args, **kwargs)
    return wrapper
    