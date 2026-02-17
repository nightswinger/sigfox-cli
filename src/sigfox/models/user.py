"""User models for Sigfox API."""

from pydantic import BaseModel, ConfigDict, Field


class MinRole(BaseModel):
    """Minimal role reference (nested in user responses)."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    path: list[dict] | None = None


class MinGroup(BaseModel):
    """Minimal group reference (nested in user responses)."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    type: int | None = None
    level: int | None = None


class User(BaseModel):
    """Sigfox user (read response model).

    Maps to the 'user' definition in the Sigfox API v2 spec.
    These are human portal users, distinct from API users.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    first_name: str | None = Field(None, alias="firstName")
    last_name: str | None = Field(None, alias="lastName")
    email: str | None = None
    timezone: str | None = None
    creation_time: int | None = Field(None, alias="creationTime")
    last_login_time: int | None = Field(None, alias="lastLoginTime")
    group: MinGroup | None = None
    user_roles: list[MinRole] | None = Field(None, alias="userRoles")
    actions: list[str] | None = None
    resources: list[str] | None = None


class UserCreate(BaseModel):
    """Data for creating a new user.

    Maps to 'userCreation' in the Sigfox API v2 spec.
    Required: groupId, firstName, lastName, email, timezone, roleIds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    group_id: str = Field(alias="groupId")
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    email: str
    timezone: str
    role_ids: list[str] = Field(alias="roleIds")


class UserUpdate(BaseModel):
    """Data for updating a user.

    Maps to 'userEdition' in the Sigfox API v2 spec.
    All fields optional.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    first_name: str | None = Field(None, alias="firstName")
    last_name: str | None = Field(None, alias="lastName")
    email: str | None = None
    timezone: str | None = None
    role_ids: list[str] | None = Field(None, alias="roleIds")
