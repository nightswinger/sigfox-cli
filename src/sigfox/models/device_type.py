"""Device type models for Sigfox API."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Group(BaseModel):
    """Nested group information."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None


class Contract(BaseModel):
    """Nested contract information."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None


class DeviceType(BaseModel):
    """Sigfox device type."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    name: str | None = None
    description: str | None = None
    group: Group | None = None
    contract: Contract | None = None
    keep_alive: int | None = Field(None, alias="keepAlive")
    alert_email: str | None = Field(None, alias="alertEmail")
    payload_type: int | None = Field(None, alias="payloadType")
    payload_config: str | None = Field(None, alias="payloadConfig")
    downlink_mode: int | None = Field(None, alias="downlinkMode")
    downlink_data_string: str | None = Field(None, alias="downlinkDataString")
    automatic_renewal: bool | None = Field(None, alias="automaticRenewal")
    creation_time: int | None = Field(None, alias="creationTime")
    last_edited_time: int | None = Field(None, alias="lastEditedTime")


class DeviceTypeCreate(BaseModel):
    """Data for creating a new device type."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str
    group_id: str = Field(alias="groupId")
    description: str | None = None
    keep_alive: int | None = Field(None, alias="keepAlive")
    alert_email: str | None = Field(None, alias="alertEmail")
    payload_type: int | None = Field(None, alias="payloadType")
    payload_config: str | None = Field(None, alias="payloadConfig")
    downlink_mode: int | None = Field(None, alias="downlinkMode")
    downlink_data_string: str | None = Field(None, alias="downlinkDataString")
    automatic_renewal: bool | None = Field(None, alias="automaticRenewal")


class DeviceTypeUpdate(BaseModel):
    """Data for updating a device type."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str | None = None
    description: str | None = None
    keep_alive: int | None = Field(None, alias="keepAlive")
    alert_email: str | None = Field(None, alias="alertEmail")
    payload_type: int | None = Field(None, alias="payloadType")
    payload_config: str | None = Field(None, alias="payloadConfig")
    downlink_mode: int | None = Field(None, alias="downlinkMode")
    downlink_data_string: str | None = Field(None, alias="downlinkDataString")
    automatic_renewal: bool | None = Field(None, alias="automaticRenewal")
