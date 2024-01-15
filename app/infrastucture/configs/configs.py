from pydantic.v1 import BaseSettings


class PostgresSettings(BaseSettings):
    db: str
    user: str
    password: str
    host: str
    port: str

    class Config:
        env_prefix = "postgres_"
