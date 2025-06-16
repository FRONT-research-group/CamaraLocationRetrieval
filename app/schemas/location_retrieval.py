from typing import Optional, List,Annotated
from enum import Enum
from datetime import datetime

from ipaddress import IPv4Address, IPv6Address

from pydantic import BaseModel, Field, IPvAnyAddress, AnyHttpUrl,RootModel


class PhoneNumber(RootModel[str]):
    root: Annotated[
        str,
        Field(
            description="A public identifier addressing a telephone subscription. In mobile networks it corresponds to the MSISDN (Mobile Station International Subscriber Directory Number). In order to be globally unique it has to be formatted in international format, according to E.164 standard, prefixed with '+'.",
            examples=["+123456789"],
            pattern="^\\+[1-9][0-9]{4,14}$",
        ),
    ]


class NetworkAccessIdentifier(RootModel[str]):
    root: Annotated[
        str,
        Field(
            description="A public identifier addressing a subscription in a mobile network. In 3GPP terminology, it corresponds to the GPSI formatted with the External Identifier ({Local Identifier}@{Domain Identifier}). Unlike the telephone number, the network access identifier is not subjected to portability ruling in force, and is individually managed by each operator.",
            examples=["123456789@domain.com"],
        ),
    ]


class SingleIpv4Addr(RootModel[IPv4Address]):
    root: Annotated[
        IPv4Address,
        Field(
            description="A single IPv4 address with no subnet mask",
            examples=["203.0.113.0"],
        ),
    ]


class Port(RootModel[int]):
    root: Annotated[int, Field(description="TCP or UDP port number", ge=0, le=65535)]


class DeviceIpv4Addr1(BaseModel):
    publicAddress: SingleIpv4Addr
    privateAddress: SingleIpv4Addr
    publicPort: Port | None = None


class DeviceIpv4Addr2(BaseModel):
    publicAddress: SingleIpv4Addr
    privateAddress: SingleIpv4Addr | None = None
    publicPort: Port


class DeviceIpv4Addr(RootModel[DeviceIpv4Addr1 | DeviceIpv4Addr2]):
    root: Annotated[
        DeviceIpv4Addr1 | DeviceIpv4Addr2,
        Field(
            description="The device should be identified by either the public (observed) IP address and port as seen by the application server, or the private (local) and any public (observed) IP addresses in use by the device (this information can be obtained by various means, for example from some DNS servers).\n\nIf the allocated and observed IP addresses are the same (i.e. NAT is not in use) then  the same address should be specified for both publicAddress and privateAddress.\n\nIf NAT64 is in use, the device should be identified by its publicAddress and publicPort, or separately by its allocated IPv6 address (field ipv6Address of the Device object)\n\nIn all cases, publicAddress must be specified, along with at least one of either privateAddress or publicPort, dependent upon which is known. In general, mobile devices cannot be identified by their public IPv4 address alone.\n",
            examples=[{"publicAddress": "203.0.113.0", "publicPort": 59765}],
        ),
    ]


class DeviceIpv6Address(RootModel[IPv6Address]):
    root: Annotated[
        IPv6Address,
        Field(
            description="The device should be identified by the observed IPv6 address, or by any single IPv6 address from within the subnet allocated to the device (e.g. adding ::0 to the /64 prefix).\n",
            examples=["2001:db8:85a3:8d3:1319:8a2e:370:7344"],
        ),
    ]


class Device(BaseModel):
    phoneNumber: PhoneNumber | None = None
    networkAccessIdentifier: NetworkAccessIdentifier | None = None
    ipv4Address: DeviceIpv4Addr | None = None
    ipv6Address: DeviceIpv6Address | None = None
    
class RetrievalLocationRequest(BaseModel):
    """
    Request to retrieve the location of a device. Device is not required when using a 3-legged access token.
    """
    device: Optional[Device] = Field(None,description="End-user device able to connect to a mobile network.")
    maxAge: Optional[int] = Field(None, description="Maximum age of the location information which is accepted for the location retrieval (in seconds).")
    maxSurface: Optional[int] = Field(None,description="Maximum surface in square meters which is accepted by the client for the location retrieval.")


class AreaType(str,Enum):
    circle = "CIRCLE" # The area is defined as a circle.
    polygon = "POLYGON" # The area is defined as a polygon.


class Area(RootModel[AreaType]):
    root: Annotated[
        AreaType,
        Field(description="""
            Type of this area.
            CIRCLE - The area is defined as a circle.
            POLYGON - The area is defined as a polygon.
            """)]

class Point(BaseModel):
    latitude: Annotated[float,Field(description="Latitude component of a location.",examples=["50.735851"],ge=-90,le=90)]
    longitude: Annotated[float,Field(..., description="Longitude component of location.",examples=["7.10066"],ge=-180,le=180)]

class PointList(RootModel[Annotated[
        List[Point],
        Field(min_length=3,max_length=15, description="List of points defining the area.")]]):
    pass

class Circle(8):
    center: Point = Field(..., description="Center point of the circle.")
    radius: float = Field(..., description="Radius of the circle.")

class Polygon(BaseModel):
    boundary: PointList = Field(..., description="List of points defining the polygon.")

class LastLocationTime(BaseModel):
    timestamp: datetime = Field(..., description="Last date and time when the device was localized.")

class ErrorInfo(BaseModel):
    status: int = Field(..., description="HTTP status code returned along with this error response.")
    code: str = Field(..., description="Code given to this error.")
    message: str = Field(..., description="Detailed error description.")

class Location(BaseModel):
    lastLocationTime: LastLocationTime = Field(..., description="Last known location time.")
    area: Area = Field(..., description="Geographical area of the location.")