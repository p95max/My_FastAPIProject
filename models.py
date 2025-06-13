from sqlalchemy import Column, Integer, String, DateTime, Text, func, ForeignKey, Table
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

Base = declarative_base()

class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    lost_items:Mapped[list['LostItem']] = relationship("LostItem", back_populates="category")
    found_items:Mapped[list['FoundItem']] = relationship("FoundItem", back_populates="category")

lostitem_tag = Table(
    'lostitem_tag',
    Base.metadata,
    Column('lost_item_id', ForeignKey('lost_items.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True)
)

lostitem_tag = Table(
    'founditem_tag',
    Base.metadata,
    Column('found_item_id', ForeignKey('found_items.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True)
)

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)

    lost_items:Mapped[list['LostItem']] = relationship("LostItem", secondary='lostitem_tag', back_populates="tags")
    found_items:Mapped[list['FoundItem']] = relationship("FoundItem", secondary='founditem_tag', back_populates="tags")

class LostItem(Base):
    __tablename__ = "lost_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, default='')
    lost_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    location: Mapped[str] = mapped_column(String)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'), index=True, default=None, nullable=True)
    category: Mapped[Category] = relationship(back_populates="lost_items")

    tags: Mapped[list['Tag']] = relationship(secondary='lostitem_tag', back_populates="lost_items")

class FoundItem(Base):
    __tablename__ = "found_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, default='')
    found_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    location: Mapped[str] = mapped_column(String)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'), index=True, default=None, nullable=True)
    category: Mapped[Category] = relationship(back_populates="found_items")

    tags: Mapped[list['Tag']] = relationship(secondary='founditem_tag', back_populates="found_items")


