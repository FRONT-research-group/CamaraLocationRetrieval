from pydantic import ValidationError


from app.schemas.location_retrieval import (
    RetrievalLocationRequest)

from app.schemas.monitoring_event import (
    MonitoringEventSubscriptionRequest,
    MonitoringType,
    LocationType,
    DurationSec
)

from app.config import get_settings

settings = get_settings()

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

    if settings.location_type == "current_location":
        return MonitoringEventSubscriptionRequest(
            msisdn=retrieve_location_request.device.phoneNumber.root.lstrip("+"),
            notificationDestination=settings.notification_destination,
            monitoringType=MonitoringType.LOCATION_REPORTING,
            locationType=LocationType.CURRENT_LOCATION,
            maximumNumberOfReports=3,
            repPeriod=DurationSec(root=20)
        )
    else:
        return MonitoringEventSubscriptionRequest(
            msisdn=retrieve_location_request.device.phoneNumber.root.lstrip("+"),
            notificationDestination=settings.notification_destination,
            monitoringType=MonitoringType.LOCATION_REPORTING,
            locationType=LocationType.LAST_KNOWN
        )

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
        
        return subscription_3gpp