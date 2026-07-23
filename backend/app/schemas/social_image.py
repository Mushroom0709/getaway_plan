from pydantic import BaseModel
from typing import Optional

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
