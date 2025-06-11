from pydantic import BaseModel, ConfigDict
from datetime import datetime


# LostItems
class LostItemBase(BaseModel):
    name: str
    description: str = None
    lost_date: datetime = None
    location: str
    category_id: int | None = None


class LostItemCreate(LostItemBase):
    pass


class LostItemUpdate(BaseModel):
    name: str = None
    description: str = None
    lost_date: datetime = None
    location: str = None
    category_id: int | None = None


class LostItem(LostItemBase):
    id: int


# FoundtItems
class FoundItemBase(BaseModel):
    name: str
    description: str = None
    found_date: datetime = None
    location: str
    category_id: int | None = None


class FoundItemCreate(FoundItemBase):
    pass


class FoundItemUpdate(BaseModel):
    name: str = None
    description: str = None
    found_date: datetime = None
    location: str = None
    category_id: int | None = None


class FoundItem(FoundItemBase):
    id: int

class CategoryBase(BaseModel):
    name: str
    description: str = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: str = None

class CategoryInBase(CategoryBase):
    id:int



