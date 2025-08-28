from flask import Blueprint

bp = Blueprint("messages", __name__)

@bp.get("/inbox")
def inbox_placeholder():
    return {"items": [], "folder": "inbox"}, 200