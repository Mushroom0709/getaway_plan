from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.database import get_db
from app.deps import get_current_device_id
from app.models.social_image import SocialImage
from app.schemas.social_image import SocialImageCreate, SocialImageUpdate, SocialImageResponse

router = APIRouter(prefix="/api", tags=["social_image"], dependencies=[Depends(get_current_device_id)])

@router.get("/notes/{note_id}/social_images", response_model=list[SocialImageResponse])
async def list_social_images(note_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SocialImage).where(SocialImage.note_id == note_id))
    items = result.scalars().all()
    return [SocialImageResponse.model_validate(x) for x in items]

@router.post("/notes/{note_id}/social_images", response_model=SocialImageResponse, status_code=201)
async def create_social_image(note_id: int, data: SocialImageCreate, db: AsyncSession = Depends(get_db)):
    item = SocialImage(**data.model_dump())
    setattr(item, "note_id", note_id)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return SocialImageResponse.model_validate(item)

@router.put("/social_images/{item_id}", response_model=SocialImageResponse)
async def update_social_image(item_id: int, data: SocialImageUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SocialImage).where(SocialImage.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(item, key, val)
    await db.commit()
    await db.refresh(item)
    return SocialImageResponse.model_validate(item)

@router.delete("/social_images/{item_id}", status_code=204)
async def delete_social_image(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SocialImage).where(SocialImage.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    await db.delete(item)
    await db.commit()
