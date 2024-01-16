from abc import ABC, abstractmethod
from app.infrastucture.models.postgres_models import OriginalUrl, ShortenedUrl


class IUrlRepository(ABC):
    @abstractmethod
    async def find_shortened_url(self, shortened_url: str) -> ShortenedUrl:
        pass

    @abstractmethod
    async def find_original_url(self, original_url: str) -> OriginalUrl:
        pass

    @abstractmethod
    async def add_shortened_add_original_urls(self, original_url: OriginalUrl,
                                              shortened_url: ShortenedUrl) -> ShortenedUrl:
        pass

    @abstractmethod
    async def add_shortened_url(self, shortened_url: ShortenedUrl) -> ShortenedUrl:
        pass
