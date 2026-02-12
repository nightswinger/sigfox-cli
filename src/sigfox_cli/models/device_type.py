"""Device type models."""

from typing import Any

from pydantic import BaseModel, Field


class DeviceTypeGroup(BaseModel):
    """Group information for device type."""

    id: str | None = None
    name: str | None = None
    type: int | None = None


class DeviceTypeContract(BaseModel):
    """Contract information for device type."""

    id: str | None = None
    name: str | None = None


class DeviceTypeDetail(BaseModel):
    """Full Sigfox device type model for API responses."""

    model_config = {"extra": "allow"}

    id: str = Field(description="Device type identifier")
    name: str = Field(description="Device type name")
    description: str | None = Field(None, description="Device type description")
    group: DeviceTypeGroup | None = Field(None, description="Associated group")
    contract: DeviceTypeContract | None = Field(None, description="Associated contract")
    keep_alive: int | None = Field(None, alias="keepAlive", description="Keep alive period in seconds (0 = default)")
    alert_email: str | None = Field(None, alias="alertEmail", description="Alert email address")
    payload_type: int | None = Field(
        None,
        alias="payloadType",
        description="Payload type (2=Regular, 3=Custom grammar, 4=Geolocation, 5=Display, 6=Radio planning, 9=Sensitv2)",
    )
    payload_config: str | None = Field(None, alias="payloadConfig", description="Payload config (custom grammar)")
    downlink_mode: int | None = Field(
        None,
        alias="downlinkMode",
        description="Downlink mode (0=DIRECT, 1=CALLBACK, 2=NONE, 3=MANAGED)",
    )
    downlink_data_string: str | None = Field(None, alias="downlinkDataString", description="Downlink data (hex)")
    automatic_renewal: bool | None = Field(None, alias="automaticRenewal")
    creation_time: int | None = Field(None, alias="creationTime")
    last_edited_time: int | None = Field(None, alias="lastEditedTime")


class DeviceTypeCreate(BaseModel):
    """Model for creating a device type (POST body)."""

    name: str = Field(description="Device type name")
    group_id: str = Field(alias="groupId", description="Group ID to associate")
    description: str | None = Field(None, description="Device type description")
    keep_alive: int | None = Field(None, alias="keepAlive", description="Keep alive period in seconds")
    alert_email: str | None = Field(None, alias="alertEmail", description="Alert email address")
    payload_type: int | None = Field(None, alias="payloadType", description="Payload type")
    downlink_mode: int | None = Field(None, alias="downlinkMode", description="Downlink mode")
    downlink_data_string: str | None = Field(None, alias="downlinkDataString", description="Downlink data (hex)")
    contract_id: str | None = Field(None, alias="contractId", description="Contract ID")


class DeviceTypeUpdate(BaseModel):
    """Model for updating a device type (PUT body)."""

    name: str | None = Field(None, description="Device type name")
    description: str | None = Field(None, description="Device type description")
    keep_alive: int | None = Field(None, alias="keepAlive", description="Keep alive period in seconds")
    alert_email: str | None = Field(None, alias="alertEmail", description="Alert email address")
    payload_type: int | None = Field(None, alias="payloadType", description="Payload type")
    downlink_mode: int | None = Field(None, alias="downlinkMode", description="Downlink mode")
    downlink_data_string: str | None = Field(None, alias="downlinkDataString", description="Downlink data (hex)")


class DeviceTypeList(BaseModel):
    """Device type list response."""

    data: list[DeviceTypeDetail] = Field(default_factory=list)
    paging: dict[str, Any] | None = None
