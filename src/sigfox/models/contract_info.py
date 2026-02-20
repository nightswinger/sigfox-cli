"""Contract info models for Sigfox API."""

from pydantic import BaseModel, ConfigDict, Field


class MinGroup(BaseModel):
    """Minimal group reference (nested in contract info responses)."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    type: int | None = None
    level: int | None = None
    actions: list[str] | None = None
    resources: list[str] | None = None


class MinDeviceType(BaseModel):
    """Minimal device type reference (nested in contract info responses)."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    project_id: str | None = Field(None, alias="projectId")


class MinContractInfo(BaseModel):
    """Minimal contract info reference (e.g. for 'order' field)."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    actions: list[str] | None = None
    resources: list[str] | None = None


class ContractInfoOption(BaseModel):
    """A premium option activated in a contract."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    parameters: dict | None = None


class ContractInfo(BaseModel):
    """Sigfox contract info (read response model).

    Maps to the 'contractInfo' definition in the Sigfox API v2 spec.
    Combines fields from 'commonContractInfo' and 'contractInfo'.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None

    # From commonContractInfo
    activation_end_time: int | None = Field(None, alias="activationEndTime")
    communication_end_time: int | None = Field(None, alias="communicationEndTime")
    bidir: bool | None = None
    high_priority_downlink: bool | None = Field(None, alias="highPriorityDownlink")
    max_uplink_frames: int | None = Field(None, alias="maxUplinkFrames")
    max_downlink_frames: int | None = Field(None, alias="maxDownlinkFrames")
    max_tokens: int | None = Field(None, alias="maxTokens")
    automatic_renewal: bool | None = Field(None, alias="automaticRenewal")
    renewal_duration: int | None = Field(None, alias="renewalDuration")
    options: list[ContractInfoOption] | None = None

    # From contractInfo
    contract_id: str | None = Field(None, alias="contractId")
    user_id: str | None = Field(None, alias="userId")
    group: MinGroup | None = None
    order: MinContractInfo | None = None
    pricing_model: int | None = Field(None, alias="pricingModel")
    created_by: str | None = Field(None, alias="createdBy")
    last_edition_time: int | None = Field(None, alias="lastEditionTime")
    creation_time: int | None = Field(None, alias="creationTime")
    last_edited_by: str | None = Field(None, alias="lastEditedBy")
    start_time: int | None = Field(None, alias="startTime")
    timezone: str | None = None
    subscription_plan: int | None = Field(None, alias="subscriptionPlan")
    token_duration: int | None = Field(None, alias="tokenDuration")
    blacklisted_territories: list[MinGroup] | None = Field(
        None, alias="blacklistedTerritories"
    )
    tokens_in_use: int | None = Field(None, alias="tokensInUse")
    tokens_used: int | None = Field(None, alias="tokensUsed")
    device_type: MinDeviceType | None = Field(None, alias="deviceType")
    actions: list[str] | None = None
    resources: list[str] | None = None
