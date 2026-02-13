"""Sigfox API models."""

from .device import Device, DeviceCreate, DeviceType, DeviceUpdate
from .device_type import (
    Contract,
    DeviceType as DeviceTypeModel,
    DeviceTypeCreate,
    DeviceTypeUpdate,
    Group as GroupRef,  # Renamed: minimal group ref nested in DeviceType
)
from .group import (
    GeolocPayload,
    Group,
    GroupCallbackError,
    GroupCreate,
    GroupUpdate,
    MinGroup,
)
from .message import DeviceInfo, Message
from .pagination import PaginatedResponse, Paging

__all__ = [
    # Device models
    "Device",
    "DeviceCreate",
    "DeviceUpdate",
    "DeviceType",
    # Device type models
    "DeviceTypeModel",
    "DeviceTypeCreate",
    "DeviceTypeUpdate",
    "GroupRef",
    "Contract",
    # Group models
    "Group",
    "GroupCreate",
    "GroupUpdate",
    "GroupCallbackError",
    "GeolocPayload",
    "MinGroup",
    # Message models
    "Message",
    "DeviceInfo",
    # Pagination
    "PaginatedResponse",
    "Paging",
]
