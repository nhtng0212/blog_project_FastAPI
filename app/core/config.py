from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Blog API Assignment"
    DEBUG: bool = True

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    
    # Auth (day)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRSH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Post (h)
    POST_EXPIRE_HOURS: int = 1
    
    # Comment (h)
    COMMENT_EXPIRE_MINUTES: int = 1

    # AWS
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_S3_BUCKET_NAME: str = ""
    AWS_S3_REGION: str = "ap-southeast-1"

    class Config:
        env_file = ".env"


settings = Settings()
