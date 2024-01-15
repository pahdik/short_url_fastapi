from pydantic import BaseModel, HttpUrl


# TODO: handle the error returned by HttpUrl
class UrlSchema(BaseModel):
    url_name: HttpUrl


class ShortenedURlSchema(BaseModel):
    url_name: str


class CustomUrlSchema(BaseModel):
    original_url_name: HttpUrl
    custom_url_name: str
