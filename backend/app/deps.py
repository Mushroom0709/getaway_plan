from fastapi import Request, HTTPException, Depends
from app.services.auth_service import decode_token

async def get_current_device_id(request: Request) -> str:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = auth.split(" ", 1)[1]
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token expired or invalid")
    return payload["device_id"]
