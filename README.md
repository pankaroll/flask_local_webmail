# Local Webmail (Flask + PostgreSQL)
## 1. Description:
Local webmail for company use. Users can register and login to their account. Messages send only in local domain (@mailo.local)

---

## 2. Features
### MVP:
- User login and registration
- Sending mail to one recipient
- Inbox and Sent folders
- Mark message as read
### Secure:
- Passwords stored as secure hash (bcrypt/argon2)
- Cookie-based session (HttpOnly, Secure, SameSite)

---

## 3. Tech Stack
- **Backend**: Python + Flask
- **Database**: PostgreSQL
- **ORM / DB tools**: SQLAlchemy + Alembic (migrations)
- **Authentication**: Flask sessions (cookies)
- **Testing**: Pytest
- **Environment**: Podman (for PostgreSQL) + Virtualenv/Poetry

