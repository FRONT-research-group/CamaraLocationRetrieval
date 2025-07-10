
import requests
from pydantic import BaseModel

from app.utils.exception_errors import CoreHttpError

APPLICATION_JSON = "application/json"

def _make_request(method: str, url: str, data=None):
    try:
        headers = None
        if method == "POST" or method == "PUT":
            headers = {
                "Content-Type": APPLICATION_JSON,
                "accept": APPLICATION_JSON,
            }
        elif method == "GET":
            headers = {
                "accept": APPLICATION_JSON,
            }
        response = requests.request(method, url, headers=headers, data=data)
        response.raise_for_status()
        if response.content:
            return response.json()
    except requests.exceptions.HTTPError as e:
        raise CoreHttpError(e) from e
    except requests.exceptions.ConnectionError as e:
        raise CoreHttpError("connection error") from e
    
def monitoring_event_post(
    base_url: str, scs_as_id: str, model_payload: BaseModel
) -> dict:
    data = model_payload.model_dump_json(exclude_none=True, by_alias=True)
    url = monitoring_event_build_url(base_url, scs_as_id)
    return _make_request("POST", url, data=data)

def monitoring_event_build_url(base_url: str, scs_as_id: str, session_id: str = None):
    url = f"{base_url}/3gpp-monitoring-event/v1/{scs_as_id}/subscriptions"
    if session_id is not None and len(session_id) > 0:
        return f"{url}/{session_id}"
    else:
        return url
    