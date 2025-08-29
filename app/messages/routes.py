from datetime import datetime, timezone
from flask import Blueprint, request, g
from sqlalchemy import select, desc

from ..core.auth import login_required
from ..db import db
from ..db.models import User, Message

bp = Blueprint("messages", __name__)


def serialize_message(m: Message, me_id: int | None = None) -> dict:
    return {
        "id": m.id,
        "from": m.sender.email if m.sender else None,
        "to": m.recipient.email if m.recipient else None,
        "subject": m.subject,
        "body": m.body,
        "created_at": m.created_at.isoformat(),
        "read_at": m.read_at.isoformat() if m.read_at else None,
        "is_mine": m.sender_id == me_id,
    }


@bp.post("/")
@login_required
def send_message():
    data = request.get_json(silent=True) or {}
    to_email = (data.get("to") or "").strip().lower()
    subject = (data.get("subject") or "").strip() or None
    body = data.get("body") or ""

    if not to_email or not body:
        return {"error": "to and body required"}, 400

    recipient = db.session.execute(
        select(User).where(User.email == to_email, User.is_active.is_(True))
    ).scalar_one_or_none()
    if not recipient:
        return {"error": "recipient not found or inactive"}, 404

    m = Message(
        sender_id=g.current_user.id,
        recipient_id=recipient.id,
        subject=subject,
        body=body,
    )
    db.session.add(m)
    db.session.commit()
    return {"id": m.id}, 201


@bp.get("/inbox")
@login_required
def inbox():
    q = (
        select(Message)
        .where(
            Message.recipient_id == g.current_user.id,
            Message.is_deleted_by_recipient.is_(False),
        )
        .order_by(desc(Message.created_at))
    )
    items = [
        serialize_message(m, me_id=g.current_user.id)
        for m in db.session.scalars(q).all()
    ]
    return {"items": items, "folder": "inbox"}, 200


@bp.get("/sent")
@login_required
def sent():
    q = (
        select(Message)
        .where(
            Message.sender_id == g.current_user.id,
            Message.is_deleted_by_sender.is_(False),
        )
        .order_by(desc(Message.created_at))
    )
    items = [
        serialize_message(m, me_id=g.current_user.id)
        for m in db.session.scalars(q).all()
    ]
    return {"items": items, "folder": "sent"}, 200


@bp.get("/<int:message_id>")
@login_required
def get_message(message_id: int):
    m = db.session.get(Message, message_id)
    if not m or (
        m.sender_id != g.current_user.id and m.recipient_id != g.current_user.id
    ):
        return {"error": "not found"}, 404
    if m.sender_id == g.current_user.id and m.is_deleted_by_sender:
        return {"error": "not found"}, 404
    if m.recipient_id == g.current_user.id and m.is_deleted_by_recipient:
        return {"error": "not found"}, 404

    if m.recipient_id == g.current_user.id and m.read_at is None:
        m.read_at = datetime.now(timezone.utc)
        db.session.commit()

    return serialize_message(m, me_id=g.current_user.id), 200


@bp.post("/<int:message_id>/read")
@login_required
def mark_read(message_id: int):
    m = db.session.get(Message, message_id)
    if not m or m.recipient_id != g.current_user.id:
        return {"error": "not found"}, 404
    if m.read_at is None:
        m.read_at = datetime.now(timezone.utc)
        db.session.commit()
    return {"id": m.id, "read_at": m.read_at.isoformat()}, 200


@bp.delete("/<int:message_id>")
@login_required
def delete_message(message_id: int):
    m = db.session.get(Message, message_id)
    if not m or (
        m.sender_id != g.current_user.id and m.recipient_id != g.current_user.id
    ):
        return {"error": "not found"}, 404

    changed = False
    if m.sender_id == g.current_user.id and not m.is_deleted_by_sender:
        m.is_deleted_by_sender = True
        changed = True
    if m.recipient_id == g.current_user.id and not m.is_deleted_by_recipient:
        m.is_deleted_by_recipient = True
        changed = True

    if changed:
        db.session.commit()
    return {"id": m.id, "deleted": True}, 200
