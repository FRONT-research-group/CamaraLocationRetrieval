import uuid
from fastapi import APIRouter, Response, status, Request

from app.schemas.location_retrieval import RetrievalLocationRequest, Location
from app.services.location_retrieval_tf import create_monitoring_event_subscription
router = APIRouter()



@router.post(
        "/retrieve",
        description="Retrieve the area where a certain user device is localized.",
        tags=["Location retrieval"],
        responses={status.HTTP_200_OK:{"model": Location, "description": "Location retrieval result"}},
        response_model_exclude_unset=True)
async def retrieve_location(request: Request, sub_req: RetrievalLocationRequest, response: Response) -> None:
    if(request.headers.get("x-correlator")):
        response.headers["x-correlator"] = request.headers.get("x-correlator")
    else:
        x_correlator_id = uuid.uuid4()
        response.headers["x-correlator"] = str(x_correlator_id)

    return create_monitoring_event_subscription(sub_req)