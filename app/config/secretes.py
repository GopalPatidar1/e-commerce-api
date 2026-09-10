from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_URL: str
    DB_URL_SYNC: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    RAZOR_PAY_KEY: str
    RAZOR_PAY_SECRET: str
    RAZOR_CALLBACK_URL: str
    RAZORPAY_WEBHOOK_SECRET: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

secretes = Settings()