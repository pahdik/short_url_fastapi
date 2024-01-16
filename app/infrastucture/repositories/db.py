from abc import ABC, abstractmethod
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import joinedload

from app.domain.interfaces.interface_repositories import IOriginalUrlRepository, IShortenedUrlRepository
from app.infrastucture.models.postgres_models import OriginalUrl, ShortenedUrl, Base
from app.infrastucture.configs.configs import PostgresSettings

settings = PostgresSettings()

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.user}:{settings.password}@{settings.host}:5432/{settings.db}"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class OriginalUrlRepository(IOriginalUrlRepository):

    async def __aenter__(self):
        self.session = async_session()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc:
            await self.session.rollback()

        await self.session.close()

    async def add_one(self, model: OriginalUrl) -> None:
        self.session.add(model)
        await self.session.commit()

    async def find_one(self, original_url: str) -> OriginalUrl | None:
        query = (
            select(OriginalUrl)
            .where(OriginalUrl.original_url == original_url)
            .options(joinedload(OriginalUrl.shortened_urls))
        )
        result = await self.session.execute(query)

        found_original_url = result.unique().scalars().one_or_none()
        return found_original_url


class ShortenedUrlRepository(IShortenedUrlRepository):
    async def __aenter__(self):
        self.session = async_session()

    async def __aexit__(self, exc_type, exc, tb):
        if exc:
            await self.session.rollback()
        await self.session.close()

    async def add_one(self, model: ShortenedUrl) -> None:
        self.session.add(model)
        await self.session.commit()

    async def find_one(self, shortened_url: str) -> ShortenedUrl | None:
        query = (
            select(ShortenedUrl)
            .options(joinedload(ShortenedUrl.original_url, innerjoin=True))
            .where(ShortenedUrl.shortened_url == shortened_url)
        )
        result = await self.session.execute(query)
        return result.unique().scalars().one_or_none()
