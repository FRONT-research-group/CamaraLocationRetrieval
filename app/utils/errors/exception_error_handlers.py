from fastapi import Request
from fastapi.exceptions import RequestValidationError
from app.schemas.location_retrieval import BadRequestError,NotFound404, UnauthorizedError
from app.utils.errors.exception_errors import BadRequestException,LocationInfoNotFoundException,NotFoundException, UnauthorizedException, CoreUnauthorizedException
from app.utils.logger import get_app_logger

logger = get_app_logger(__name__)

def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error("Validation error: %s",exc)

    error_response_instance = BadRequestError.model_validate({'status': 400, 'code': 'INVALID_ARGUMENT', 'message': 'Client specified an invalid argument, request body or query param.'})

    raise BadRequestException(error_response_instance)


def location_info_exception_handler(request: Request, exc: LocationInfoNotFoundException):
    logger.error("Location info not found: %s",exc)

    error_response_instance = NotFound404.model_validate({'status': 404, 'code': 'IDENTIFIER_NOT_FOUND', 'message': 'Device identifier not found.'})

    raise NotFoundException(error_response_instance)

def unauthorized_exception_handler(request: Request, exc: CoreUnauthorizedException):
    logger.error("Unauthorized access: %s",exc)
    
    error_response_instance = UnauthorizedError.model_validate({'status': 401, 'code': 'UNAUTHENTICATED', 'message': 'Request not authenticated due to missing, invalid, or expired credentials.'})

    raise UnauthorizedException(error_response_instance)