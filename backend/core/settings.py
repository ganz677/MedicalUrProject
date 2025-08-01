import os

from pathlib import Path

from dotenv import load_dotenv

from pydantic import (
    BaseModel,
    PostgresDsn
)
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)

load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

BASE_DIR =Path(__file__).parent.parent

class DataBaseSettings(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 5
    max_overflow: int = 10

class AuthJWT(BaseModel):
    algorithm: str = 'RS256'
    access_token_lifetime_seconds: int = 9600
    private_key_path: Path = BASE_DIR / 'certs' / 'private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'public.pem'
    
class FrontSettings(BaseModel):
    templates_dir: Path = BASE_DIR / 'templates'
    secret_key: str

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='APP__',
        env_nested_delimiter='__',
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra='ignore',
        populate_by_name=True
    )
    front: FrontSettings
    db: DataBaseSettings
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()


print(settings.front.secret_key)
