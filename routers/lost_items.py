import schemas
import models
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, delete
from database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.LostItem)
async def create_lost_item(item: schemas.LostItemCreate, db: AsyncSession = Depends(get_db)):
    db_item = models.LostItem(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@router.get("/", response_model=list[schemas.LostItem])
async def read_lost_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.LostItem))
    items = result.scalars().all()
    return items


@router.get("/{item_id}", response_model=schemas.LostItem)
async def read_lost_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.LostItem).where(models.LostItem.id == item_id))
    item = result.scalars().first()
    return item


@router.get("/search", response_model=list[schemas.LostItem])
async def search_lost_items(query: str, db: AsyncSession = Depends(get_db)):
    """
    Вернет список потерянных предметов, у которых имя, описание или местоположение содержат слово query.
    """
    search = await db.execute(select(models.LostItem)
        .where(
        or_(
        models.LostItem.location.ilike(query)),
        models.LostItem.name.ilike(query),
        models.LostItem.description.ilike(query)),
    )
    items = search.scalars().all()
    return items


@router.put("/{item_id}", response_model=schemas.LostItem)
async def update_lost_item(item_id: int, item: schemas.LostItemUpdate, db: AsyncSession = Depends(get_db)):
    db_item = await db.get(models.LostItem, item_id)
    for field, value in item.model_dump(exclude_none=True).items():
        setattr(db_item, field, value)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@router.delete("/{item_id}", status_code=204)
async def delete_lost_item(item_id: int, db: AsyncSession = Depends(get_db)):
    to_delete = await db.execute(delete(models.LostItem).where(models.LostItem.id == item_id))
    await db.commit()