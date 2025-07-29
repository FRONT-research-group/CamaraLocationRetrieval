import uuid
from fastapi import APIRouter, Response, status, Request

# from app.utils.exception_errors import CoreHttpError
from app.schemas.location_retrieval import RetrievalLocationRequest, Location, BadRequestError, UnauthorizedError,ForbiddenError,NotFound404,UnprocessableEntityError
from app.services.location_retrieval_tf import retrieve_location_info
from app.utils.logger import get_app_logger


log = get_app_logger()

router = APIRouter()



@router.post(
        "/retrieve",
        description="Retrieve the area where a certain user device is localized.",
        tags=["Location retrieval"],
        responses={
            status.HTTP_200_OK: {"model": Location, "description": "Location retrieval result"},
            status.HTTP_400_BAD_REQUEST: {"model": BadRequestError, "description": "Bad Request"},
            status.HTTP_401_UNAUTHORIZED: {"model": UnauthorizedError, "description": "Unauthorized"},
            status.HTTP_403_FORBIDDEN: {"model": ForbiddenError, "description": "Forbidden"},
            status.HTTP_404_NOT_FOUND: {"model": NotFound404, "description": "Not Found"},
            status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": UnprocessableEntityError, "description": "Unprocessable Entity"}
        },
        response_model_exclude_unset=True)
async def retrieve_location(request: Request, sub_req: RetrievalLocationRequest, response: Response) -> Location | None:
    if(request.headers.get("x-correlator")):
        response.headers["x-correlator"] = request.headers.get("x-correlator")
    else:
        x_correlator_id = uuid.uuid4()
        response.headers["x-correlator"] = str(x_correlator_id)

    # try:
        return retrieve_location_info(sub_req)
    # except CoreHttpError as e:
    #     log.error(f"Core HTTP error occurred: {e}")
    #     return response