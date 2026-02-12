"""Device models."""

from typing import Any

from pydantic import BaseModel, Field


class DeviceType(BaseModel):
    """Minimal device type information."""

    id: str | None = None
    name: str | None = None


class Group(BaseModel):
    """Minimal group information."""

    id: str | None = None
    name: str | None = None
    type: int | None = None


class Device(BaseModel):
    """Sigfox device model."""

    model_config = {"extra": "allow"}

    id: str = Field(description="Device identifier (hexadecimal)")
    name: str | None = Field(None, description="Device name")
    device_type: DeviceType | None = Field(None, alias="deviceType", description="Device type")
    group: Group | None = Field(None, description="Group")
    pac: str = Field(description="Porting Access Code")
    last_com: int | None = Field(None, alias="lastCom", description="Last communication timestamp")
    state: int = Field(
        description="Device state (0=OK, 1=DEAD, 2=OFF_CONTRACT, 3=DISABLED, 5=DELETED, 6=SUSPENDED, 7=NOT_ACTIVABLE)"
    )
    com_state: int = Field(
        alias="comState",
        description="Communication state (0=NO, 1=OK, 3=RED, 4=N/A, 5=NOT_SEEN)",
    )
    lqi: int | None = Field(None, description="Link Quality Indicator")
    creation_time: int | None = Field(None, alias="creationTime")
    activation_time: int | None = Field(None, alias="activationTime")
    sequence_number: int | None = Field(None, alias="sequenceNumber")
    satellite_capable: bool | None = Field(None, alias="satelliteCapable")
    repeater: bool | None = Field(None, alias="repeater")
    automatic_renewal: bool | None = Field(None, alias="automaticRenewal")


class DeviceList(BaseModel):
    """Device list response."""

    data: list[Device] = Field(default_factory=list)
    paging: dict[str, Any] | None = None
