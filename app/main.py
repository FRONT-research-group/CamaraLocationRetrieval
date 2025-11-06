from fastapi import FastAPI

from app.routers import location_retrieval

from app.config import get_settings
from app.utils.logger import get_app_logger
from app.dependencies import init_custom_exc_handlers

settings = get_settings()

logger = get_app_logger(__name__)
logger.info("Starting CAMARA LOCATION RETRIEVAL API")
logger.info("Host: %s, Port: %s", settings.host, settings.port)
logger.info("Log Directory Path: %s", settings.log_directory_path)
logger.info("Log Filename Path: %s", settings.log_filename_path)
logger.info("Base URL: %s", settings.base_url)
logger.info("SCS AS ID: %s", settings.scs_as_id)
logger.info("Location Type: %s", settings.location_type)
logger.info("Notification Destination: %s", settings.notification_destination)

app = FastAPI()

init_custom_exc_handlers(app)

uri_prefix: str = "/location-retrieval/v0.5"

app.include_router(location_retrieval.router, prefix=uri_prefix)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
