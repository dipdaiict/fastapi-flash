from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    expiration_time_of_token: int  # Assuming you want to keep this attribute

    class Config:
        env_file = ".env"

# Create an instance of the Settings class
settings = Settings()