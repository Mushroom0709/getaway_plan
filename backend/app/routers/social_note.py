from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.deps import get_current_device_id
from app.models.social_note import SocialNote
from app.models.social_image import SocialImage
from app.schemas.social_note import SocialNoteCreate, SocialNoteUpdate, SocialNoteResponse, SocialImageResponse

router = APIRouter(prefix="/api", tags=["social_notes"], dependencies=[Depends(get_current_device_id)])

@router.get("/spots/{spot_id}/notes", response_model=list[SocialNoteResponse])
async def list_notes(spot_id: int, platform: str = None, db: AsyncSession = Depends(get_db)):
    from sqlalchemy.orm import selectinload
    stmt = select(SocialNote).where(SocialNote.spot_id == spot_id).options(selectinload(SocialNote.images))
    if platform:
        stmt = stmt.where(SocialNote.platform == platform)
    result = await db.execute(stmt)
    notes = result.scalars().all()
    return [SocialNoteResponse.model_validate(n) for n in notes]

@router.post("/spots/{spot_id}/notes", response_model=SocialNoteResponse, status_code=201)
async def create_note(spot_id: int, data: SocialNoteCreate, db: AsyncSession = Depends(get_db)):
    images_data = data.images or []
    note = SocialNote(spot_id=spot_id, **data.model_dump(exclude={"images"}))
    db.add(note)
    await db.flush()
    for img in images_data:
        db.add(SocialImage(note_id=note.id, **img.model_dump()))
    await db.commit()
    from sqlalchemy.orm import selectinload
    result = await db.execute(select(SocialNote).where(SocialNote.id == note.id).options(selectinload(SocialNote.images)))
    return SocialNoteResponse.model_validate(result.scalar_one())

@router.delete("/notes/{note_id}", status_code=204)
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SocialNote).where(SocialNote.id == note_id))
    note = result.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Not found")
    await db.delete(note)
    await db.commit()
