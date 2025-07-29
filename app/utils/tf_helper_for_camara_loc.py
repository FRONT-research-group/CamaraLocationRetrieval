from datetime import datetime, timedelta, timezone
from app.services.map_render import create_map

from app.schemas.location_retrieval import (   
    Area,
    AreaType,
    Point,
    PointList,
    Polygon
)

from app.schemas.monitoring_event import (
    MonitoringEventReport
)
from app.utils.logger import get_app_logger

log = get_app_logger()

def _compute_camara_last_location_time(
    event_time: datetime, age_of_location_info_min: int = None
) -> datetime:
    """
    Computes the last location time based on the event time and age of location info.

    args:
        event_time: ISO 8601 datetime, e.g. "2025-06-18T12:30:00Z"
        age_of_location_info_min: unsigned int, age of location info in minutes

    returns:
        datetime object representing the last location time in UTC.
    """
    if age_of_location_info_min is not None:
        last_location_time = event_time - timedelta(
            minutes=age_of_location_info_min
        )
        return last_location_time.replace(tzinfo=timezone.utc)
    else:
        return event_time.replace(tzinfo=timezone.utc)
    
def build_camara_last_location_time(monitoring_event_report : MonitoringEventReport) -> datetime:
    report_event_time = monitoring_event_report.eventTime
    age_of_location_info = None

    if monitoring_event_report.locationInfo.ageOfLocationInfo is not None:
        age_of_location_info = monitoring_event_report.locationInfo.ageOfLocationInfo.duration

    last_location_time = _compute_camara_last_location_time(
        report_event_time, age_of_location_info
    )
    log.info(f"Extracted camara-specific last_location_time value: {last_location_time}")
    return last_location_time

def build_camara_area(monitoring_event_report: MonitoringEventReport) -> Area:
    geo_area = monitoring_event_report.locationInfo.geographicArea
    camara_point_list: list[Point] = []
    for point in geo_area.polygon.point_list.geographical_coords:
        camara_point_list.append(
            Point(latitude=point.lat, longitude=point.lon)
        )
    area = Polygon(
        areaType=AreaType.polygon,
        boundary=PointList(camara_point_list),
    )

    log.info(f"Extracted camara-specific area value: {area}")

    create_map(camara_point_list)

    return area