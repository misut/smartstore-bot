import pydantic


class Settings(pydantic.BaseSettings):
    USERNAME: str
    PASSWORD: str

    class Config:
        env_file = ".env"
        env_prefix = "SMARTSTORE_"
