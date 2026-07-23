from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SocialImageCreate(BaseModel):
    url: Optional[str] = None
    url_large: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    sort_order: int = 0

class SocialNoteCreate(BaseModel):
    platform: str  # xiaohongshu or douyin
    note_id: str
    title: Optional[str] = None
    author: Optional[str] = None
    author_id: Optional[str] = None
    likes: int = 0
    comments: int = 0
    shares: int = 0
    description: Optional[str] = None
    xsec_token: Optional[str] = None
    source_url: Optional[str] = None
    note_type: Optional[str] = None
    images: List[SocialImageCreate] = []

class SocialNoteUpdate(BaseModel):
    platform: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    likes: Optional[int] = None
    description: Optional[str] = None

class SocialImageResponse(BaseModel):
    id: int
    note_id: int
    url: Optional[str] = None
    url_large: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    sort_order: int = 0
    local_path: Optional[str] = None

    class Config:
        from_attributes = True

class SocialNoteResponse(BaseModel):
    id: int
    spot_id: int
    platform: str
    note_id: str
    title: Optional[str] = None
    author: Optional[str] = None
    author_id: Optional[str] = None
    likes: int = 0
    comments: int = 0
    shares: int = 0
    description: Optional[str] = None
    source_url: Optional[str] = None
    note_type: Optional[str] = None
    fetched_at: Optional[datetime] = None
    images: List[SocialImageResponse] = []

    class Config:
        from_attributes = True