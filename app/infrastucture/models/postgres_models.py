from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, DeclarativeBase
from typing import List
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


class Base(AsyncAttrs, DeclarativeBase):
    pass


class OriginalUrl(Base):
    __tablename__ = "original_urls"

    id: Mapped[int] = mapped_column(primary_key=True)
    original_url: Mapped[str] = mapped_column(String(1000), nullable=False, unique=True)
    shortened_urls: Mapped[List["ShortenedUrl"]] = relationship(back_populates="original_url", lazy='noload')


class ShortenedUrl(Base):
    __tablename__ = "shortened_urls"

    id: Mapped[int] = mapped_column(primary_key=True)
    original_url_id: Mapped[int] = mapped_column(ForeignKey("original_urls.id"))
    shortened_url: Mapped[str] = mapped_column(String(50), nullable=False)

    original_url: Mapped["OriginalUrl"] = relationship(back_populates="shortened_urls", lazy='noload')

    UniqueConstraint("original_url_id", "shortened_url", name="unique_shortened_url")
