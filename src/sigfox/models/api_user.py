"""API user models for Sigfox API."""

from pydantic import BaseModel, ConfigDict, Field


class MinProfile(BaseModel):
    """Minimal profile reference (nested in API user responses)."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    actions: list[str] | None = None


class MinGroup(BaseModel):
    """Minimal group reference (nested in API user responses)."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    type: int | None = None
    level: int | None = None


class ApiUser(BaseModel):
    """Sigfox API user (read response model).

    Maps to the 'apiUser' definition in the OpenAPI spec.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    name: str | None = None
    timezone: str | None = None
    group: MinGroup | None = None
    creation_time: int | None = Field(None, alias="creationTime")
    access_token: str | None = Field(None, alias="accessToken")
    profiles: list[MinProfile] | None = None
    actions: list[str] | None = None
    resources: list[str] | None = None


class ApiUserCreate(BaseModel):
    """Data for creating a new API user.

    Maps to 'apiUserCreation' in the OpenAPI spec.
    Required: groupId, name, timezone, profileIds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    group_id: str = Field(alias="groupId")
    name: str
    timezone: str
    profile_ids: list[str] = Field(alias="profileIds")


class ApiUserUpdate(BaseModel):
    """Data for updating an API user.

    Maps to 'apiUserEdition' in the OpenAPI spec.
    All fields optional.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str | None = None
    timezone: str | None = None
    profile_ids: list[str] | None = Field(None, alias="profileIds")
