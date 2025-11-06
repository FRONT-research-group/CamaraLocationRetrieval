from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8080
    
    log_directory_path: str = "./app/log/"
    log_filename_path: str = f"{log_directory_path}app_logger"
    
    base_url: str = "http://localhost:8000"
    scs_as_id: str = "1"
    location_type: str = "last_known" #last_known or current_location
    notification_destination: str | None = "http://127.0.0.1:8001"

    model_config = SettingsConfigDict(env_ignore_empty=True)

settings = Settings()

def get_settings() -> Settings:
    """Returns the application settings.

    This function provides access to the global settings object that contains
    all configuration parameters for the application.

    Returns:
        Settings: A Settings object containing application configuration.
    """
    return settings