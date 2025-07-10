from app.schemas.location_retrieval import (
    RetrievalLocationRequest,
    Location,
    AreaType,
    Point,
    PointList,
    Polygon)

from app.schemas.monitoring_event import (
    MonitoringEventReport
)

from app.utils.logger import get_app_logger
from app.utils.network_request_to_core import (
    monitoring_event_post
)

from app.utils.core_3gpp_subscription import (
    build_monitoring_event_subscription,
    compute_camara_last_location_time
)

from app.utils.exception_errors import NetworkPlatformError

log = get_app_logger()

def create_monitoring_event_subscription(
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
    response = monitoring_event_post(
        base_url, scs_as_id, subscription
    )

    monitoring_event_report = MonitoringEventReport(**response)
    if monitoring_event_report.locationInfo is None:
        log.error(
            "Failed to retrieve location information from monitoring event report"
        )
        raise NetworkPlatformError(
            "Location information not found in monitoring event report"
        )
    geo_area = monitoring_event_report.locationInfo.geographicArea
    report_event_time = monitoring_event_report.eventTime
    age_of_location_info = None
    if monitoring_event_report.locationInfo.ageOfLocationInfo is not None:
        age_of_location_info = (
            monitoring_event_report.locationInfo.ageOfLocationInfo.duration
        )
    last_location_time = compute_camara_last_location_time(
        report_event_time, age_of_location_info
    )
    print(f"Last Location time is {last_location_time}")
    camara_point_list: list[Point] = []
    for point in geo_area.polygon.point_list.geographical_coords:
        camara_point_list.append(
            Point(latitude=point.lat, longitude=point.lon)
        )
    camara_polygon = Polygon(
        areaType=AreaType.polygon,
        boundary=PointList(camara_point_list),
    )

    camara_location = Location(
        area=camara_polygon, lastLocationTime=last_location_time
    )

    return camara_location

