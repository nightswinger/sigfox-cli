"""Operator models for Sigfox API."""

from pydantic import BaseModel, ConfigDict, Field


class MinGroup(BaseModel):
    """Minimal group reference (nested in operator responses)."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    type: int | None = None
    level: int | None = None


class Operator(BaseModel):
    """Sigfox operator (read response model).

    Maps to the 'operator' definition in the Sigfox API v2 spec.
    Operators represent Sigfox Network Operators (SNOs).
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    name: str | None = None
    group: MinGroup | None = None
    host_operator: bool | None = Field(None, alias="hostOperator")
    contract_id: str | None = Field(None, alias="contractId")
    creation_time: int | None = Field(None, alias="creationTime")
    actions: list[str] | None = None
    resources: list[str] | None = None
