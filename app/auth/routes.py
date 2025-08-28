from flask import Blueprint

bp = Blueprint("auth", __name__)

@bp.get("/login")
def login_placeholder():
    return {"message": "login OK"}, 200