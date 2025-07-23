
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.schemas.location_retrieval import BadRequestError
from app.utils.logger import get_app_logger

logger = get_app_logger()

def validation_exception_handler(request,exc: RequestValidationError):
    logger.error(f"Validation error: {exc}")


    error_response_instance = BadRequestError.model_validate({'status': 400, 'code': 'INVALID_ARGUMENT', 'message': 'Client specified an invalid argument, request body or query param.'})
    response_status = error_response_instance.status
    response_code = error_response_instance.code
    response_message = error_response_instance.message

    return JSONResponse(
        status_code=response_status, 
        content=response_message,
        headers={"code": response_code} 
    )

