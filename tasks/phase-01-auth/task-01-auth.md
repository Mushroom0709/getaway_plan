# S2: 认证模块 — 登录 + JWT 认证中间件

## Goal

实现 FastAPI 认证模块：后端骨架入口 + JWT 认证中间件 + auth 路由。

## Acceptance Criteria

- [ ] POST /api/auth/login 接受密码，返回 JWT token
- [ ] 错误密码返回 401
- [ ] GET /api/auth/verify 验证 token 有效性
- [ ] 未带 token 访问受保护接口返回 401

## Recipe

### 文件 1: backend/app/config.py
```python
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "mysql+aiomysql://root:password@localhost:3306/getaway_plan"
    jwt_secret: str = "dev-secret-change-in-production"
    access_password_hash: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

### 文件 2: backend/app/database.py
```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import settings

engine = create_async_engine(settings.database_url, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
```

### 文件 3: backend/app/models/auth_token.py
```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime, timezone

class Base(DeclarativeBase):
    pass

class AuthToken(Base):
    __tablename__ = "auth_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(200), nullable=False, index=True)
    token = Column(String(500), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
```

### 文件 4: backend/app/schemas/auth.py
```python
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
```

### 文件 5: backend/app/services/auth_service.py
```python
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
```

### 文件 6: backend/app/deps.py
```python
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
```

### 文件 7: backend/app/routers/auth.py
```python
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
```

### 文件 8: backend/app/routers/__init__.py
```python
from app.routers.auth import router as auth_router
```

### 文件 9: backend/app/main.py
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth_router

app = FastAPI(title="Getaway Plan API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

@app.get("/api/health")
async def health():
    return {"status": "ok"}
```

**注意：** 不要修改 BASE_PATH 或路径前缀，所有路由从 `/api/` 开始。所有文件创建后做 Python 语法检查：`python -c "import ast; ast.parse(open('FILE').read())"` 对每个文件执行。

## Verification

```bash
# 启动后端
cd /Users/mushroom/Documents/ai/hermes/projects/getaway_plan_v1
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 &
sleep 2

# 测试 health
curl -s http://localhost:8000/api/health

# 测试 login（密码错误）
curl -s -X POST http://localhost:8000/api/auth/login -H "Content-Type: application/json" -d '{"password":"wrong"}'

# 测试 verify 无 token
curl -s http://localhost:8000/api/auth/verify
```