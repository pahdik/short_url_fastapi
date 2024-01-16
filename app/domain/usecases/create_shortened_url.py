from app.domain.usecases.base_usecase import BaseUseCase
from .mixins import OriginalUrlMixin, ShortenedUrlMixin
from ..interfaces.interface_repositories import IShortenedUrlRepository, IOriginalUrlRepository
from ..schema.url_schema import UrlSchema, ShortenedURlSchema
import hashlib


def get_new_shortened_url(original_url: str) -> str:
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(original_url.encode('utf-8'))
    hashed_original_url = hash_algorithm.hexdigest()
    return hashed_original_url[:6]


class CreateShortenedUrl(BaseUseCase, OriginalUrlMixin, ShortenedUrlMixin):
    def __init__(
            self,
            shortened_url_repo: IShortenedUrlRepository,
            original_url_repo: IOriginalUrlRepository
    ):
        self.shortened_url_repo = shortened_url_repo
        self.original_url_repo = original_url_repo

    async def execute(self, original_url: UrlSchema) -> ShortenedURlSchema:
        original_url_entity = await self.get_or_add_original_url(str(original_url.url_name))
        if original_url_entity.shortened_urls:
            return ShortenedURlSchema(url_name=original_url_entity.shortened_urls[0].shortened_url)
        new_shortened_url = get_new_shortened_url(original_url_entity.original_url)
        created_shortened_url_entity = await self.add_shortened_url(original_url_entity, new_shortened_url)
        return ShortenedURlSchema(url_name=created_shortened_url_entity.shortened_url)
