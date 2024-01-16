from app.domain.usecases.base_usecase import BaseUseCase
from ..interfaces.interface_repositories import IShortenedUrlRepository
from ..schema.url_schema import UrlSchema


class GetOriginalUrl(BaseUseCase):
    def __init__(self, shortened_url_repo: IShortenedUrlRepository):
        self.shortened_url_repo = shortened_url_repo

    async def execute(self, shortened_url: str) -> UrlSchema:
        async with self.shortened_url_repo:
            result = await self.shortened_url_repo.find_one(shortened_url)
            if not result:
                raise Exception()
            return UrlSchema(url_name=result.original_url.original_url)
