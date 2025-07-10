from pydantic import ValidationError
from datetime import datetime, timedelta, timezone

from app.schemas.location_retrieval import (
    RetrievalLocationRequest)

from app.schemas.monitoring_event import (
    MonitoringEventSubscriptionRequest,
    MonitoringType,
    LocationType
)

def _core_specific_monitoring_event_validation(
        retrieve_location_request: RetrievalLocationRequest
    ) -> None:
        """Check core specific elements that required for location retrieval in NEF."""
        if retrieve_location_request.device is None:
            raise ValidationError(
                "Open5GS requires a device to be specified for location retrieval in NEF."
            )

def _add_core_specific_location_parameters(
    retrieve_location_request: RetrievalLocationRequest
) -> MonitoringEventSubscriptionRequest:
    """Add core specific location parameters to support location retrieval scenario in NEF."""
    return MonitoringEventSubscriptionRequest(
        msisdn=retrieve_location_request.device.phoneNumber.root.lstrip("+"),
        notificationDestination="http://127.0.0.1:8001",
        monitoringType=MonitoringType.LOCATION_REPORTING,
        locationType=LocationType.LAST_KNOWN,
    )
    # subscription.msisdn = retrieve_location_request.device.phoneNumber.root.lstrip('+')
    # monitoringType = schemas.MonitoringType.LOCATION_REPORTING
    # locationType = schemas.LocationType.LAST_KNOWN
    # locationType = schemas.LocationType.CURRENT_LOCATION
    # maximumNumberOfReports = 1
    # repPeriod = schemas.DurationSec(root=20)



def build_monitoring_event_subscription(
        retrieve_location_request: RetrievalLocationRequest
    ) -> MonitoringEventSubscriptionRequest:
        _core_specific_monitoring_event_validation(retrieve_location_request)
        subscription_3gpp = _add_core_specific_location_parameters(
            retrieve_location_request
        )
        device = retrieve_location_request.device
        subscription_3gpp.externalId = device.networkAccessIdentifier
        subscription_3gpp.ipv4Addr = device.ipv4Address
        subscription_3gpp.ipv6Addr = device.ipv6Address
        # subscription.msisdn = device.phoneNumber.root.lstrip('+')
        # subscription.notificationDestination = "http://127.0.0.1:8001"

        return subscription_3gpp

def compute_camara_last_location_time(
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