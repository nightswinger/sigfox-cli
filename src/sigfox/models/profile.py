"""Profile models for Sigfox API."""

from pydantic import BaseModel, ConfigDict


class MinMetaRole(BaseModel):
    """Minimal role reference within a role's path."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None


class MinRole(BaseModel):
    """Minimal role reference (nested in profile responses)."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    path: list[MinMetaRole] | None = None


class MinGroup(BaseModel):
    """Minimal group reference (nested in profile responses)."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    type: int | None = None
    level: int | None = None


class Profile(BaseModel):
    """Sigfox profile (read response model).

    Maps to the 'profile' definition in the Sigfox API v2 spec.
    Profiles define sets of roles that can be assigned to API users.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    name: str | None = None
    group: MinGroup | None = None
    roles: list[MinRole] | None = None
    actions: list[str] | None = None
    resources: list[str] | None = None
