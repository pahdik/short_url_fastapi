from abc import ABC, abstractmethod
from app.infrastucture.models.postgres_models import OriginalUrl, ShortenedUrl


class IOriginalUrlRepository(ABC):
    @abstractmethod
    async def add_one(self, model: OriginalUrl) -> OriginalUrl:
        pass

    @abstractmethod
    async def find_one(self, original_url: str) -> OriginalUrl:
        pass


class IShortenedUrlRepository(ABC):
    @abstractmethod
    async def add_one(self, model: ShortenedUrl) -> ShortenedUrl:
        pass

    @abstractmethod
    async def find_one(self, shortened_url: str) -> ShortenedUrl:
        pass
