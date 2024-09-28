from pydantic_settings import BaseSettings,SettingsConfigDict


class Settings(BaseSettings):
    FEDEX_BASE_API_URL: str
    FEDEX_API_KEY: str
    FEDEX_SECRET_KEY:str

    model_config = SettingsConfigDict(env_file=".env")
