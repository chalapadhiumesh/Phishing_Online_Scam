from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import model_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "Phishing & Scam Intelligence Platform"
    DB_HOST: str | None = None
    DB_PORT: int | None = None
    DB_NAME: str | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    SECRET_KEY: str = "default_secret_key_for_jwt_auth_must_be_changed_in_prod"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days
    GOOGLE_CLIENT_ID: str = ""
    FRONTEND_URL: str = "http://localhost:5173"
    
    SUPABASE_DATABASE_URL: str | None = None

    @property
    def DATABASE_URL(self) -> str:
        if self.SUPABASE_DATABASE_URL:
            url = self.SUPABASE_DATABASE_URL.strip().strip("'").strip('"')
            if "://" not in url:
                url = f"postgresql://{url}"
            if url.startswith("postgres://"):
                url = url.replace("postgres://", "postgresql://", 1)
            
            import re
            # Fix if the user literally pasted [password] with the brackets
            url = re.sub(r'\[(.*?)\]@', r'\1@', url)
            
            # Fix if the user has an unencoded '@' symbol in their password
            parts = url.split('@')
            if len(parts) > 2:
                credentials = "%40".join(parts[:-1])
                host_and_beyond = parts[-1]
                url = f"{credentials}@{host_and_beyond}"
                
            return url
        
        if not self.DB_HOST:
            raise ValueError("CRITICAL ERROR: SUPABASE_DATABASE_URL is missing in Render Environment Variables.")
            
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

    @model_validator(mode='after')
    def validate_secret_key(self):
        if not self.SECRET_KEY or len(self.SECRET_KEY) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long for production security.")
        return self

settings = Settings()
