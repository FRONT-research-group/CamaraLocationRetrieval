from fastapi import HTTPException
from app.schemas.location_retrieval import BadRequestError, UnauthorizedError,ForbiddenError,NotFound404,UnprocessableEntityError

class CoreHttpError(Exception):
    pass

class NetworkPlatformError(Exception):
    pass
class LocationInfoNotFoundException(Exception):
    pass

class BadRequestException(HTTPException):
    def __init__(self, bad_request_error: BadRequestError):
        super().__init__(status_code=bad_request_error.status, detail=bad_request_error.message, headers={"code": bad_request_error.code})

class UnauthorizedException(HTTPException):
    def __init__(self, unauthorized_error: UnauthorizedError):
        super().__init__(status_code=unauthorized_error.status, detail=unauthorized_error.message, headers={"code": unauthorized_error.code})

class ForbiddenException(HTTPException):
    def __init__(self, forbidden_error: ForbiddenError):
        super().__init__(status_code=forbidden_error.status, detail=forbidden_error.message, headers={"code": forbidden_error.code})

class NotFoundException(HTTPException):
    def __init__(self, not_found_error: NotFound404):
        super().__init__(status_code=not_found_error.status, detail=not_found_error.message, headers={"code": not_found_error.code})

class UnprocessableEntityException(HTTPException):
    def __init__(self, unprocessable_entity_error: UnprocessableEntityError):
        super().__init__(status_code=unprocessable_entity_error.status, detail=unprocessable_entity_error.message, headers={"code": unprocessable_entity_error.code})
