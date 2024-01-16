from app.domain.usecases.base_usecase import BaseUseCase
from ..interfaces.interface_repositories import IShortenedUrlRepository, IOriginalUrlRepository
from ..schema.url_schema import CustomUrlSchema, ShortenedURlSchema
from .mixins import OriginalUrlMixin, ShortenedUrlMixin


class CreateCustomShortenedUrl(BaseUseCase, OriginalUrlMixin, ShortenedUrlMixin):
    def __init__(
            self,
            shortened_url_repo: IShortenedUrlRepository,
            original_url_repo: IOriginalUrlRepository
    ):
        self.shortened_url_repo = shortened_url_repo
        self.original_url_repo = original_url_repo

    async def execute(self, model: CustomUrlSchema) -> ShortenedURlSchema:
        original_url_entity = await self.get_or_add_original_url(str(model.original_url_name))
        shortened_url_entity = await self.add_shortened_url(original_url_entity, model.custom_url_name)
        return ShortenedURlSchema(url_name=shortened_url_entity.shortened_url)
