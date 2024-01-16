from app.domain.usecases.base_usecase import BaseUseCase
from .custom_exeptions import DuplicateEntryError
from ..interfaces.interface_repositories import IUrlRepository
from ..schema.url_schema import CustomUrlSchema, ShortenedURlSchema
from ...infrastucture.models.postgres_models import ShortenedUrl, OriginalUrl


class CreateCustomShortenedUrl(BaseUseCase):
    def __init__(self, url_repo: IUrlRepository):
        self.url_repo = url_repo

    async def execute(self, model: CustomUrlSchema) -> ShortenedURlSchema:
        async with self.url_repo:
            shortened_url_entity = await self.url_repo.find_shortened_url(str(model.custom_url_name))

            if shortened_url_entity:
                raise DuplicateEntryError("Such a short URL already exists")

            original_url_entity = await self.url_repo.find_original_url(str(model.original_url_name))
            new_shortened_url_entity = ShortenedUrl(shortened_url=str(model.custom_url_name))

            if not original_url_entity:
                new_original_url_entity = OriginalUrl(original_url=str(model.original_url_name))
                result = await self.url_repo.add_shortened_add_original_urls(new_original_url_entity,
                                                                             new_shortened_url_entity)
                return ShortenedURlSchema(url_name=result.shortened_url)

            new_shortened_url_entity.original_url_id = original_url_entity.id
            result = await self.url_repo.add_shortened_url(new_shortened_url_entity)

            return ShortenedURlSchema(url_name=result.shortened_url)
