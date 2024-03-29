from fastapi import APIRouter
from app.domain.schema.url_schema import UrlSchema, CustomUrlSchema, ShortenedURlSchema
from app.domain.usecases.create_shortened_url import CreateShortenedUrl
from app.infrastucture.repositories.db import UrlRepository
from app.domain.usecases.get_original_url import GetOriginalUrl
from app.domain.usecases.create_custom_shortened_url import CreateCustomShortenedUrl

router = APIRouter(
    tags=["url"],
    prefix="/url"
)


@router.post("/create-short-url")
async def create_short_url(data: UrlSchema) -> ShortenedURlSchema:
    res = await CreateShortenedUrl(UrlRepository()).execute(data)
    return res


@router.post("/create-custom-url")
async def create_custom_url(data: CustomUrlSchema):
    res = await CreateCustomShortenedUrl(UrlRepository()).execute(data)
    return res


@router.get("/{short_url}")
async def get_original_url(short_url: str):
    res = await GetOriginalUrl(UrlRepository()).execute(short_url)
    return res
