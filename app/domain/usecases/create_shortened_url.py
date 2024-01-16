import random
import hashlib
from app.domain.usecases.base_usecase import BaseUseCase
from ..interfaces.interface_repositories import IUrlRepository
from ..schema.url_schema import UrlSchema, ShortenedURlSchema
from ...infrastucture.models.postgres_models import ShortenedUrl, OriginalUrl


def get_new_shortened_url(original_url: str) -> str:
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(original_url.encode('utf-8'))
    hashed_original_url = hash_algorithm.hexdigest()
    return hashed_original_url[:6]


class CreateShortenedUrl(BaseUseCase):
    def __init__(self, url_repo: IUrlRepository):
        self.url_repo = url_repo

    async def execute(self, model: UrlSchema) -> ShortenedURlSchema:
        async with self.url_repo:
            original_url_entity = await self.url_repo.find_original_url(str(model.url_name))

            if original_url_entity:
                return ShortenedURlSchema(url_name=original_url_entity.shortened_urls[0].shortened_url)

            new_shortened_url = get_new_shortened_url(str(model.url_name))
            stored_shortened_url_entity = await self.url_repo.find_shortened_url(new_shortened_url)

            if stored_shortened_url_entity:

                for _ in range(10):
                    new_shortened_url = get_new_shortened_url(str(model.url_name) + str(random.randint(1, 10000)))
                    stored_shortened_url_entity = await self.url_repo.find_shortened_url(new_shortened_url)

                    if not stored_shortened_url_entity:
                        break
                else:
                    raise Exception()

            new_shortened_url_entity = ShortenedUrl(shortened_url=new_shortened_url)
            new_original_url_entity = OriginalUrl(original_url=str(model.url_name))

            result = await self.url_repo.add_shortened_add_original_urls(new_original_url_entity,
                                                                         new_shortened_url_entity)
            return ShortenedURlSchema(url_name=result.shortened_url)
