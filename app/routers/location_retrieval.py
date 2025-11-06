import uuid
from typing import Annotated
from fastapi import APIRouter, Response, status, Header, Depends
from app.schemas.location_retrieval import (
    RetrievalLocationRequest, XCorrelator, Location,
    BadRequestError, UnauthorizedError, ForbiddenError,
    NotFound404, UnprocessableEntityError
)
from app.services.location_retrieval_tf import retrieve_location_info
from app.utils.logger import get_app_logger


log = get_app_logger(__name__)

router = APIRouter()


async def get_xcorrelator(x_correlator: Annotated[XCorrelator | None, 
                                                  Header(description="Correlation id for the different services.",
                                                         examples=["b4333c46-49c0-4f62-80d7-f0ef930f1c46"],
                                                         include_in_schema=True)] = None
                          ) -> XCorrelator:
    """
        Retrieve and validate an X-Correlator value from the incoming request header.

        This function is intended to be used as a FastAPI dependency for extracting the
        "X-Correlator" header. If the header is absent, a new UUIDv4 string will be
        generated and used as the correlator value. The resulting value is validated
        and returned as an instance of XCorrelator.

        Parameters
        ----------
        x_correlator: XCorrelator | None
            The value provided by the "X-Correlator" request header. If None, a new
            UUIDv4 string will be generated. The header annotation includes a description
            and an example for OpenAPI documentation.

        Returns
        -------
        XCorrelator
            A validated XCorrelator instance created from the header value or the
            generated UUID.

        Raises
        ------
        ValidationError
            If the final correlator value (header or generated) cannot be validated by
            XCorrelator.model_validate.
    """
    if x_correlator is None:
        x_correlator = str(uuid.uuid4())

    log.info("The x-correlator header value that going to be used is: %s", x_correlator)

    return XCorrelator.model_validate(x_correlator)


x_correlator_header = {
    "description": "Correlation id for the different services",
    "schema": {"$ref": "#/components/schemas/XCorrelator"},
    "example": "b4333c46-49c0-4f62-80d7-f0ef930f1c46",
}


@router.post(
    "/retrieve",
    description="Retrieve the area where a certain user device is localized.",
    tags=["Location retrieval"],
    responses={
        status.HTTP_200_OK: {
            "model": Location,
            "description": "Location retrieval result",
            "headers": {"x-correlator": x_correlator_header},
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": BadRequestError,
            "description": "Bad Request",
            "headers": {"x-correlator": x_correlator_header},
        },
        status.HTTP_401_UNAUTHORIZED: {
            "model": UnauthorizedError,
            "description": "Unauthorized",
            "headers": {"x-correlator": x_correlator_header},
        },
        status.HTTP_403_FORBIDDEN: {
            "model": ForbiddenError,
            "description": "Forbidden",
            "headers": {"x-correlator": x_correlator_header},
        },
        status.HTTP_404_NOT_FOUND: {
            "model": NotFound404,
            "description": "Not Found",
            "headers": {"x-correlator": x_correlator_header},
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": UnprocessableEntityError,
            "description": "Unprocessable Entity",
            "headers": {"x-correlator": x_correlator_header},
        },
    },
    response_model_exclude_unset=True)
async def retrieve_location(x_correlator: Annotated[XCorrelator, Depends(get_xcorrelator)], sub_req: RetrievalLocationRequest, response: Response) -> Location | None:
    response.headers["x-correlator"] = x_correlator.root
    return retrieve_location_info(sub_req)
