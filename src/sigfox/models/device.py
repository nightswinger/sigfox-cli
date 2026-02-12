"""Device models for Sigfox API."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class DeviceType(BaseModel):
    """Nested device type information."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None


class Device(BaseModel):
    """Sigfox device."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    name: str | None = None
    device_type: DeviceType | None = Field(None, alias="deviceType")
    state: int | None = None
    com_state: int | None = Field(None, alias="comState")
    last_com: int | None = Field(None, alias="lastCom")
    creation_time: int | None = Field(None, alias="creationTime")
    activation_time: int | None = Field(None, alias="activationTime")
    pac: str | None = None
    sequence_number: int | None = Field(None, alias="sequenceNumber")
    lqi: int | None = None
    satellite_capable: bool | None = Field(None, alias="satelliteCapable")
    repeater: bool | None = None
    automatic_renewal: bool | None = Field(None, alias="automaticRenewal")
    lat: float | None = None
    lng: float | None = None
    prototype: bool | None = None
    activable: bool | None = None


class DeviceCreate(BaseModel):
    """Data for creating a new device."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    name: str
    device_type_id: str = Field(alias="deviceTypeId")
    pac: str
    lat: float | None = None
    lng: float | None = None
    product_certificate: str | None = Field(None, alias="productCertificate")
    prototype: bool | None = None
    automatic_renewal: bool | None = Field(None, alias="automaticRenewal")
    activable: bool | None = None


class DeviceUpdate(BaseModel):
    """Data for updating a device."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str | None = None
    lat: float | None = None
    lng: float | None = None
    product_certificate: str | None = Field(None, alias="productCertificate")
    prototype: bool | None = None
    automatic_renewal: bool | None = Field(None, alias="automaticRenewal")
    activable: bool | None = None
