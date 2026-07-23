from pydantic import BaseModel
from datetime import datetime

class LoginRequest(BaseModel):
    password: str

class LoginResponse(BaseModel):
    token: str
    expires_at: datetime

class VerifyResponse(BaseModel):
    valid: bool
    expires_at: datetime | None = None
