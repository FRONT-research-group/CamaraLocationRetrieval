
import requests
from pydantic import BaseModel

from app.utils.errors.exception_errors import CoreHttpError, LocationInfoNotFoundException, NetworkPlatformError, CoreUnauthorizedException
from app.utils.logger import get_app_logger
from app.invoker_onboarding.invoker_capif_connector import onboard_invoker
from app.config import get_settings

log = get_app_logger(__name__)
settings = get_settings()

APPLICATION_JSON = "application/json"

def _make_request(method: str, url: str, data=None):
    jwt_token = onboard_invoker()
    try:
        headers = None
        if method == "POST" or method == "PUT":
            headers = {
                "Content-Type": APPLICATION_JSON,
                "accept": APPLICATION_JSON,
                "Authorization": "Bearer " + jwt_token
            }
        elif method == "GET":
            headers = {
                "accept": APPLICATION_JSON,
                "Authorization": "Bearer " + jwt_token
            }
        log.info("Making %s request to %s with headers %s and data %s",method, url, headers, data)
        response = requests.request(method, url, headers=headers, data=data, timeout=10)
        response.raise_for_status()
        if response.content:
            return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            raise CoreUnauthorizedException(e) from e
        elif e.response.status_code == 404:
            raise LocationInfoNotFoundException(e) from e
        raise CoreHttpError(e) from e
    except requests.exceptions.ConnectionError as e:
        raise CoreHttpError("connection error") from e
    
def monitoring_event_post_request(
    base_url: str, scs_as_id: str, model_payload: BaseModel
) -> dict:
    data = model_payload.model_dump_json(exclude_none=True, by_alias=True)
    url = _monitoring_event_build_url(base_url, scs_as_id)
    try:
        return _make_request("POST", url, data=data)
    except CoreHttpError as exc:
        log.error("Failed to post monitoring event: %s", exc)
        raise NetworkPlatformError("Failed to post monitoring event") from exc

def _monitoring_event_build_url(base_url: str, scs_as_id: str, session_id: str = None):
    if settings.project_api_name is None or settings.project_api_name == "":
        url = f"{base_url}/3gpp-monitoring-event/v1/{scs_as_id}/subscriptions"
    else:
        url= f"{base_url}" + "/3gpp-monitoring-event-" + settings.project_api_name + "/v1/"+ f"{scs_as_id}/subscriptions"
    if session_id is not None and len(session_id) > 0:
        return f"{url}/{session_id}"
    else:
        return url
    