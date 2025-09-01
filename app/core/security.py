from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password: str) -> str:
    return generate_password_hash(password, method="pbkdf2:sha256", salt_length=16)


def verify_password(password: str, password_hash: str) -> bool:
    return check_password_hash(password_hash, password)
