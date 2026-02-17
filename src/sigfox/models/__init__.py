"""Sigfox API models."""

from .api_user import (
    ApiUser,
    ApiUserCreate,
    ApiUserUpdate,
    MinGroup as ApiUserMinGroup,
    MinProfile,
)
from .base_station import (
    BaseStation,
    BaseStationUpdate,
    MessageBaseStation,
    MinBaseStation,
)
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
from .user import (
    MinGroup as UserMinGroup,
    MinRole,
    User,
    UserCreate,
    UserUpdate,
)

__all__ = [
    # API User models
    "ApiUser",
    "ApiUserCreate",
    "ApiUserUpdate",
    "ApiUserMinGroup",
    "MinProfile",
    # Base Station models
    "BaseStation",
    "BaseStationUpdate",
    "MessageBaseStation",
    "MinBaseStation",
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
    # User models
    "User",
    "UserCreate",
    "UserUpdate",
    "UserMinGroup",
    "MinRole",
]
