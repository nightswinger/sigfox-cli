"""Group models for Sigfox API."""

from pydantic import BaseModel, ConfigDict, Field


class MinGroup(BaseModel):
    """Minimal group reference (used in path arrays)."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    type: int | None = None
    level: int | None = None


class Group(BaseModel):
    """Sigfox group (read response model).

    Maps to the 'group' definition in the OpenAPI spec.
    The 'type' field encodes group kind:
      0=SO, 2=Basic/Other, 5=SVNO, 6=Partners,
      7=NIP, 8=DIST, 9=Channel, 10=Starter, 11=Partner
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    name: str | None = None
    description: str | None = None
    type: int | None = None
    timezone: str | None = None
    name_ci: str | None = Field(None, alias="nameCI")
    path: list[MinGroup] | None = None
    created_by: str | None = Field(None, alias="createdBy")
    creation_time: int | None = Field(None, alias="creationTime")
    leaf: bool | None = None
    actions: list[str] | None = None
    is_account: bool | None = Field(None, alias="isAccount")
    # Fields from billableGroup (present on Basic, Partners, Channel, etc.)
    billable: bool | None = None
    technical_email: str | None = Field(None, alias="technicalEmail")
    max_prototype_allowed: int | None = Field(None, alias="maxPrototypeAllowed")
    current_prototype_count: int | None = Field(None, alias="currentPrototypeCount")
    # Fields from SO/NIP subtypes
    country_iso_alpha3: str | None = Field(None, alias="countryISOAlpha3")
    # Fields from SVNO/DIST subtypes
    network_operator_id: str | None = Field(None, alias="networkOperatorId")


class GroupCreate(BaseModel):
    """Data for creating a new group.

    Maps to 'commonGroupCreate' in the OpenAPI spec.
    Required: name, description, type, timezone, parentId.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str
    description: str
    type: int
    timezone: str
    parent_id: str = Field(alias="parentId")
    technical_email: str | None = Field(None, alias="technicalEmail")
    account_id: str | None = Field(None, alias="accountId")
    # Optional subtype-specific fields
    network_operator_id: str | None = Field(None, alias="networkOperatorId")
    country_iso_alpha3: str | None = Field(None, alias="countryISOAlpha3")
    # Billable group fields
    billable: bool | None = None
    max_prototype_allowed: int | None = Field(None, alias="maxPrototypeAllowed")


class GroupUpdate(BaseModel):
    """Data for updating a group.

    Maps to 'commonGroupUpdate' in the OpenAPI spec.
    All fields optional (PUT only updates provided fields).
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str | None = None
    description: str | None = None
    type: int | None = None
    timezone: str | None = None
    # Billable group fields
    billable: bool | None = None
    technical_email: str | None = Field(None, alias="technicalEmail")
    max_prototype_allowed: int | None = Field(None, alias="maxPrototypeAllowed")


class GroupCallbackError(BaseModel):
    """Undelivered callback error message for a group.

    Maps to 'groupErrorMessages' in the OpenAPI spec.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    device: str | None = None
    device_url: str | None = Field(None, alias="deviceUrl")
    device_type: str | None = Field(None, alias="deviceType")
    time: int | None = None
    data: str | None = None
    snr: str | None = None
    status: str | None = None
    message: str | None = None
    callback: dict | None = None
    parameters: dict | None = None


class GeolocPayload(BaseModel):
    """Geolocation payload for a group.

    Maps to 'baseGeolocation' in the OpenAPI spec.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
