from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str

    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    FILE_DEFULT_CHUNK_SIZE:int
    MONGODB_URL :str
    MONGODB_DATABSE :str
    


    class Config:
        env_file = ".env"

model_config = SettingsConfigDict(env_file=".env")
def get_settings():
    return Settings()