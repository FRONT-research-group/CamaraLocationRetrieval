from fastapi import FastAPI

from app.routers import location_retrieval

from app.config import get_settings
from app.utils.logger import get_app_logger


settings = get_settings()

logger = get_app_logger()
logger.info("Starting CAMARA LOCATION RETRIEVAL API")
logger.info(f"Host: {settings.host}, Port: {settings.port}")
logger.info(f"Log Directory Path: {settings.log_directory_path}")
logger.info(f"Log Filename Path: {settings.log_filename_path}")
logger.info(f"Base URL: {settings.base_url}")
logger.info(f"SCS AS ID: {settings.scs_as_id}")
logger.info(f"Location Type: {settings.location_type}")
logger.info(f"Notification Destination: {settings.notification_destination}")

app = FastAPI()

app.include_router(location_retrieval.router,prefix="/location-retrieval/v0.4",tags=["Location retrieval"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)