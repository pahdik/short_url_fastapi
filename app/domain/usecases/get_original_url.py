from pydantic import HttpUrl
from app.domain.usecases.base_usecase import BaseUseCase
from .custom_exeptions import NotFoundError
from ..interfaces.interface_repositories import IUrlRepository
from ..schema.url_schema import UrlSchema


class GetOriginalUrl(BaseUseCase):
    def __init__(self, url_repo: IUrlRepository):
        self.url_repo = url_repo

    async def execute(self, shortened_url: str) -> UrlSchema:
        async with self.url_repo:
            result = await self.url_repo.find_shortened_url(shortened_url)

            if not result:
                raise NotFoundError(f"URL '{shortened_url}' was not found")

            res = HttpUrl(result.original_url.original_url)
            return UrlSchema(url_name=res)
