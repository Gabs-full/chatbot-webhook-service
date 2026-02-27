from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    OPENAI_KEY: str = ""
    CLAUDE_KEY: str = ""
    EVOLUTION_URL: str = ""
    EVOLUTION_KEY: str = ""
    ZAPI_TOKEN: str = ""
    ZAPI_SECURITY_TOKEN: str = ""

    model_config = {"env_file": ".env", "case_sensitive": False, "extra": "ignore"}



settings = Settings()
