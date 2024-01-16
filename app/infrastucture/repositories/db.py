from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import joinedload
from app.domain.interfaces.interface_repositories import IUrlRepository
from app.infrastucture.configs.configs import PostgresSettings
from app.infrastucture.models.postgres_models import OriginalUrl, ShortenedUrl, Base

settings = PostgresSettings()

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.user}:{settings.password}@{settings.host}:5432/{settings.db}"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class UrlRepository(IUrlRepository):
    async def __aenter__(self):
        self.session = async_session()

    async def __aexit__(self, exc_type, exc, tb):
        if exc:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()

    async def find_shortened_url(self, shortened_url: str) -> ShortenedUrl:
        query = (
            select(ShortenedUrl)
            .options(joinedload(ShortenedUrl.original_url, innerjoin=True))
            .where(ShortenedUrl.shortened_url == shortened_url)
        )
        result = await self.session.execute(query)
        return result.unique().scalars().one_or_none()

    async def find_original_url(self, original_url: str) -> OriginalUrl:
        query = (
            select(OriginalUrl)
            .where(OriginalUrl.original_url == original_url)
            .options(joinedload(OriginalUrl.shortened_urls))
        )
        result = await self.session.execute(query)

        return result.unique().scalars().one_or_none()

    async def add_shortened_add_original_urls(self, original_url: OriginalUrl,
                                              shortened_url: ShortenedUrl) -> ShortenedUrl:
        shortened_url.original_url = original_url
        self.session.add(original_url)
        self.session.add(shortened_url)
        return shortened_url

    async def add_shortened_url(self, shortened_url: ShortenedUrl) -> ShortenedUrl:
        self.session.add(shortened_url)
        return shortened_url
