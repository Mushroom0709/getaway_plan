import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from app.config import settings

def verify_password(plain: str, hashed: str) -> bool:
    if not hashed:
        return False
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

def create_access_token(device_id: str) -> dict:
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    payload = {"device_id": device_id, "exp": expires_at}
    token = jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
    return {"token": token, "expires_at": expires_at}

def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
