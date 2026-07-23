from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.deps import get_current_device_id
from app.models.social_image import SocialImage
from app.schemas.social_image import SocialImageResponse

router = APIRouter(prefix="/api", tags=["social_images"], dependencies=[Depends(get_current_device_id)])

@router.get("/notes/{note_id}/images", response_model=list[SocialImageResponse])
async def list_images(note_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SocialImage).where(SocialImage.note_id == note_id).order_by(SocialImage.sort_order))
    items = result.scalars().all()
    return [SocialImageResponse.model_validate(x) for x in items]

@router.delete("/images/{image_id}", status_code=204)
async def delete_image(image_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SocialImage).where(SocialImage.id == image_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    await db.delete(item)
    await db.commit()