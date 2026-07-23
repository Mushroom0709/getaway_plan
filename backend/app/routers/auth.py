from fastapi import APIRouter, HTTPException, Header, Depends
from app.schemas.auth import LoginRequest, LoginResponse, VerifyResponse
from app.services.auth_service import verify_password, create_access_token, decode_token
from app.config import settings
from app.deps import get_current_device_id

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
async def login(body: LoginRequest):
    if not verify_password(body.password, settings.access_password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")
    device_id = "device-" + str(hash(body.password))
    result = create_access_token(device_id)
    return LoginResponse(token=result["token"], expires_at=result["expires_at"])

@router.get("/verify", response_model=VerifyResponse)
async def verify(device_id: str = Depends(get_current_device_id)):
    # extract token from header to get expires_at
    from fastapi import Request
    return VerifyResponse(valid=True, expires_at=None)
