"""Message models."""

from typing import Any

from pydantic import BaseModel, Field


class MessageDevice(BaseModel):
    """Device information in message."""

    id: str | None = None
    name: str | None = None


class DeviceMessage(BaseModel):
    """Sigfox device message model."""

    model_config = {"extra": "allow"}

    device: MessageDevice | None = None
    time: int = Field(description="Message timestamp (milliseconds since Unix epoch)")
    data: str | None = Field(None, description="Message payload (hex encoded)")
    ack_required: bool | None = Field(None, alias="ackRequired")
    lqi: int | None = Field(
        None,
        description="Link Quality Indicator (0=LIMIT, 1=AVERAGE, 2=GOOD, 3=EXCELLENT, 4=NA)",
    )
    lqi_repeaters: int | None = Field(None, alias="lqiRepeaters")
    seq_number: int | None = Field(
        None,
        alias="seqNumber",
        description="Sequence number (may not be present for V0 protocol)",
    )
    nb_frames: int | None = Field(None, alias="nbFrames", description="Number of frames (1 or 3)")
    computed_location: list[dict[str, Any]] | None = Field(None, alias="computedLocation")
    rinfos: list[dict[str, Any]] | None = None


class MessageList(BaseModel):
    """Message list response."""

    data: list[DeviceMessage] = Field(default_factory=list)
    paging: dict[str, Any] | None = None
