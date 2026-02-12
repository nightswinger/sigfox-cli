"""Pagination models for Sigfox API."""

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class Paging(BaseModel):
    """Pagination information."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    next: str | None = None
    previous: str | None = Field(None, alias="prev")


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated API response."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    data: list[T]
    paging: Paging | None = None
