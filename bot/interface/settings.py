import pydantic


class Settings(pydantic.BaseSettings):
    USERNAME: str
    PASSWORD: str

    class Config:
        env_path = ".env"
        env_prefix = "SMARTSTORE_"
