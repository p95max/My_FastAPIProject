import schemas
import models
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from database import get_db
from tools import hashed_password, validate_password, create_access_token

router = APIRouter()

@router.post("/reg", status_code=201)
async def registation(item: schemas.CreateUser, db: AsyncSession = Depends(get_db)):
    if item.password != item.password2:
        raise HTTPException(status_code=400, detail="Passwords not match")

    user = models.User(username=item.username, password=hashed_password(item.password))
    db.add(user)
    await db.commit()
    return {}


@router.post("/auth")
async def user_auth(item: schemas.AuthUser, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).where(models.User.username == item.username))
    items = result.scalars().first()
    if not validate_password(item.password, items.password):
        raise HTTPException(status_code=401, detail="Access Denied")
    token = create_access_token(data={"sub": items.username})
    return token

