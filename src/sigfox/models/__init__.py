"""Sigfox API models."""

from .device import Device, DeviceCreate, DeviceType, DeviceUpdate
from .device_type import (
    Contract,
    DeviceType as DeviceTypeModel,
    DeviceTypeCreate,
    DeviceTypeUpdate,
    Group,
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
    "Group",
    "Contract",
    # Message models
    "Message",
    "DeviceInfo",
    # Pagination
    "PaginatedResponse",
    "Paging",
]
