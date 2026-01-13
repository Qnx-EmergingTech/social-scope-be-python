from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    FACEBOOK_APP_ID: str
    FACEBOOK_APP_SECRET_KEY: str
    FACEBOOK_URL: str
    USER_ACCESS_TOKEN: str

    OPENAI_URL: str
    OPENAI_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
