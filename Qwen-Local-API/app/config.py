from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    OLLAMA_URL: str

    OLLAMA_MODEL: str

    REQUEST_TIMEOUT: int

    class Config:
        env_file = ".env"


settings = Settings()