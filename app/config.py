from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8080
    log_directory_path: str = "./app/log/"
    log_filename_path: str = f"{log_directory_path}app_logger"
    base_url: str = "http://localhost:8000"
    scs_as_id: str = "1"
    location_type: str = "last_known" #last_known or current_location
    notification_destination: str | None = "http://127.0.0.1:8001"

settings = Settings()

def get_settings() -> Settings:
    return settings