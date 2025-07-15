from app.schemas.location_retrieval import (
    RetrievalLocationRequest,
    Location)

from app.schemas.monitoring_event import (
    MonitoringEventReport
)

from app.utils.logger import get_app_logger
from app.utils.network_request_to_core import (
    monitoring_event_post_request
)

from app.utils.tf_to_3gpp_subscription import (
    build_monitoring_event_subscription
)

from app.utils.tf_helper_for_camara_loc import (
    build_camara_last_location_time,
    build_camara_area
)
from app.config import get_settings
from app.utils.exception_errors import NetworkPlatformError

log = get_app_logger()
settings = get_settings()

def retrieve_location_info(
    retrieve_location_request: RetrievalLocationRequest
) -> Location:
    """
    Creates a Monitoring Event subscription based on CAMARA Location API input.

    args:
        retrieve_location_request: Dictionary containing location retrieval details conforming to
                                    the CAMARA Location API parameters.

    returns:
        dictionary containing the created subscription details, including its ID.
    """
    subscription = build_monitoring_event_subscription(
        retrieve_location_request
    )
    
    response = monitoring_event_post_request(
        settings.base_url, settings.scs_as_id, subscription
    )

    monitoring_event_report = MonitoringEventReport(**response)
    if monitoring_event_report.locationInfo is None:
        log.error(
            "Failed to retrieve location information from monitoring event report"
        )
        raise NetworkPlatformError(
            "Location information not found in monitoring event report"
        )
    
    area = build_camara_area(monitoring_event_report)
    last_location_time = build_camara_last_location_time(monitoring_event_report)

    camara_location = Location(
        area=area, lastLocationTime=last_location_time
    )

    return camara_location

