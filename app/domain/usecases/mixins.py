from app.domain.usecases.custom_exeptions import DuplicateEntryError
from app.infrastucture.models.postgres_models import OriginalUrl, ShortenedUrl


class OriginalUrlMixin:
    async def get_or_add_original_url(self, original_url: str) -> OriginalUrl:
        async with self.original_url_repo as repo:
            result = await repo.find_one(original_url)
            if result:
                return result
            new_original_url_entity = OriginalUrl(original_url=original_url)
            await repo.add_one(new_original_url_entity)
            return new_original_url_entity


class ShortenedUrlMixin:
    async def add_shortened_url(self, original_url_entity: OriginalUrl, new_shortened_url: str) -> ShortenedUrl:
        async with self.shortened_url_repo:
            found_url = await self.shortened_url_repo.find_one(new_shortened_url)
            if found_url:
                raise DuplicateEntryError("Such a short URL already exists")
            new_shortened_url_entity = ShortenedUrl(
                shortened_url=new_shortened_url,
                original_url_id=original_url_entity.id,
            )
            await self.shortened_url_repo.add_one(new_shortened_url_entity)
            return new_shortened_url_entity