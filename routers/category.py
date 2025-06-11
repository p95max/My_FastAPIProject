import schemas
import models
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.CategoryInBase)
async def create_category(item: schemas.CategoryCreate, db: AsyncSession = Depends(get_db)):
    db_item = models.Category(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@router.get("/", response_model=list[schemas.CategoryInBase])
async def read_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Category))
    items = result.scalars().all()
    return items


@router.get("/{item_id}", response_model=schemas.CategoryInBase)
async def read_category(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Category).where(models.Category.id == item_id))
    item = result.scalars().first()
    return item



@router.put("/{item_id}", response_model=schemas.CategoryInBase)
async def update_category(item_id: int, item: schemas.CategoryUpdate, db: AsyncSession = Depends(get_db)):
    db_item = await db.get(models.Category, item_id)
    for field, value in item.model_dump(exclude_none=True).items():
        setattr(db_item, field, value)
    await db.commit()
    await db.refresh(db_item)
    return db_item


@router.delete("/{item_id}", status_code=204)
async def delete_category(item_id: int, db: AsyncSession = Depends(get_db)):
    to_delete = await db.execute(delete(models.Category).where(models.Category.id == item_id))
    await db.commit()
