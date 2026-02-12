"""Message models for Sigfox API."""

from pydantic import BaseModel, ConfigDict, Field


class DeviceInfo(BaseModel):
    """Nested device information in message."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None


class Message(BaseModel):
    """Sigfox message."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    time: int | None = None
    device: DeviceInfo | None = None
    data: str | None = None
    seq_number: int | None = Field(None, alias="seqNumber")
    lqi: int | None = None
    nb_frames: int | None = Field(None, alias="nbFrames")
    operator: str | None = None
    country: str | None = None
    computed_location: dict | None = Field(None, alias="computedLocation")
