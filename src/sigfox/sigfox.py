"""Sigfox API client facade."""

from .api import ApiUsersAPI, BaseStationsAPI, CoveragesAPI, DevicesAPI, DeviceTypesAPI, GroupsAPI, UsersAPI
from .client import SigfoxClient


class Sigfox:
    """High-level Sigfox API client.

    This is the main entry point for interacting with the Sigfox API.
    It provides typed, Pythonic interfaces to all API operations.

    Example:
        >>> client = Sigfox(login="api_login", password="api_password")
        >>> devices = client.devices.list(limit=10)
        >>> for device in devices:
        ...     print(device.id, device.name)
    """

    def __init__(
        self,
        login: str,
        password: str,
        base_url: str = "https://api.sigfox.com/v2",
        timeout: int = 30,
    ):
        """Initialize Sigfox API client.

        Args:
            login: Sigfox API login (ID)
            password: Sigfox API password (secret)
            base_url: API base URL
            timeout: Request timeout in seconds
        """
        self._client = SigfoxClient(
            api_login=login,
            api_password=password,
            base_url=base_url,
            timeout=timeout,
        )
        self.api_users = ApiUsersAPI(self._client)
        self.base_stations = BaseStationsAPI(self._client)
        self.coverages = CoveragesAPI(self._client)
        self.devices = DevicesAPI(self._client)
        self.device_types = DeviceTypesAPI(self._client)
        self.groups = GroupsAPI(self._client)
        self.users = UsersAPI(self._client)

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def close(self):
        """Close the underlying HTTP client."""
        self._client.close()
