from pydantic import BaseModel, ConfigDict
from datetime import datetime

#User auth
class CreateUser(BaseModel):
    username: str
    password: str
    password2: str

class AuthUser(BaseModel):
    username: str
    password: str

# Categories and tags
class CategoryBase(BaseModel):
    name: str
    description: str = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: str = None

class CategoryInBase(CategoryBase):
    id:int

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagUpdate(TagBase):
    pass

class TagInBase(TagBase):
    id:int

# LostItems
class LostItemBase(BaseModel):
    name: str
    description: str = None
    lost_date: datetime = None
    location: str
    category_id: int | None = None
    tags: list[TagInBase] = []

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
    tags: list[TagInBase] = []


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







