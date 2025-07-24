
from fastapi.exceptions import RequestValidationError
from app.schemas.location_retrieval import BadRequestError,NotFound404
from app.utils.errors.exception_errors import BadRequestException,LocationInfoNotFoundException,NotFoundException
from app.utils.logger import get_app_logger

logger = get_app_logger()

def validation_exception_handler(request,exc: RequestValidationError):
    logger.error(f"Validation error: {exc}")

    error_response_instance = BadRequestError.model_validate({'status': 400, 'code': 'INVALID_ARGUMENT', 'message': 'Client specified an invalid argument, request body or query param.'})

    raise BadRequestException(error_response_instance)


def location_info_exception_handler(request,exc: LocationInfoNotFoundException):
    logger.error(f"Location info not found: {exc}")

    error_response_instance = NotFound404.model_validate({'status': 404, 'code': 'IDENTIFIER_NOT_FOUND', 'message': 'Device identifier not found.'})

    raise NotFoundException(error_response_instance)

