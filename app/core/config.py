from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    CLERK_JWT_ISSUER: str
    CLERK_JWT_AUDIENCE: str

    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str

    FREE_MONTHLY_CREDITS: int = 20
    PRO_MONTHLY_CREDITS: int = 500

    ENABLE_AI_GENERATION: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
