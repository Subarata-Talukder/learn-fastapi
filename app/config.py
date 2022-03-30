from pydantic import BaseSettings

class Settings(BaseSettings):
    db_host:str
    db_port:int
    db_password:str
    db_name:str
    db_user_name:str
    secret_key:str
    algorithm:str
    secret_key_expire_min:int

    class Config:
        env_file = ".env"

settings = Settings()