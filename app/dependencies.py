from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.utils.errors.exception_errors import LocationInfoNotFoundException
from app.utils.errors.exception_error_handlers import validation_exception_handler, location_info_exception_handler
from app.utils.logger import get_app_logger

logger = get_app_logger()

def init_custom_exc_handlers(app: FastAPI) -> None:
    """
    Initialize custom exception handlers for the FastAPI application.
    This function should be called during the application startup.
    """
    logger.info("Initializing FastAPI application with custom exception handlers...")


    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(LocationInfoNotFoundException, location_info_exception_handler)