from sqlalchemy import Column, Integer, String, DateTime, Text, func, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

Base = declarative_base()

class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    lost_items:Mapped[list['LostItem']] = relationship("LostItem", back_populates="category")
    found_items:Mapped[list['FoundItem']] = relationship("FoundItem", back_populates="category")

class LostItem(Base):
    __tablename__ = "lost_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, default='')
    lost_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    location: Mapped[str] = mapped_column(String)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'), index=True, default=None, nullable=True)
    category: Mapped[Category] = relationship(back_populates="lost_items")



class FoundItem(Base):
    __tablename__ = "found_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, default='')
    found_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    location: Mapped[str] = mapped_column(String)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'), index=True, default=None, nullable=True)
    category: Mapped[Category] = relationship(back_populates="found_items")
