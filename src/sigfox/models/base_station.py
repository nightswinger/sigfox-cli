"""Base station models for Sigfox API."""

from pydantic import BaseModel, ConfigDict, Field


class MinBaseStation(BaseModel):
    """Minimal base station reference.

    Used in various API responses where only basic base station info is needed.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    actions: list[str] | None = None


class MessageBaseStation(BaseModel):
    """Base station information in message responses.

    Used in device messages to indicate which base station received the message.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    resource_type: int | None = Field(None, alias="resourceType")


class BaseStation(BaseModel):
    """Complete base station model.

    Represents a Sigfox base station with all available properties.
    Resource types: 0=SBS (Sigfox Base Station), 1=NAP (Network Access Point)
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    # Identity
    id: str
    name: str | None = None

    # Location
    lat: float | None = None
    lng: float | None = None
    location_country: str | None = Field(None, alias="locationCountry")

    # Group
    group: dict | None = None

    # Versioning
    version_current: str | None = Field(None, alias="versionCurrent")
    hw_version: str | None = Field(None, alias="hwVersion")
    hw_family: str | None = Field(None, alias="hwFamily")

    # Commissioning
    first_commissioning_time: int | None = Field(None, alias="firstCommissioningTime")
    commissioning_time: int | None = Field(None, alias="commissioningTime")
    decommissioning_time: int | None = Field(None, alias="decommissioningTime")
    operating_days: int | None = Field(None, alias="operatingDays")

    # Warranty
    manufacturer_delivery_time: int | None = Field(None, alias="manufacturerDeliveryTime")
    warranty_time: int | None = Field(None, alias="warrantyTime")

    # Communication
    last_communication_time: int | None = Field(None, alias="lastCommunicationTime")
    last_ping_time: int | None = Field(None, alias="lastPingTime")
    connection_type: int | None = Field(None, alias="connectionType")

    # Status
    communication_state: int | None = Field(None, alias="communicationState")
    state: int | None = None
    lifecycle_status: int | None = Field(None, alias="lifecycleStatus")

    # Configuration
    description: str | None = None
    keep_alive: int | None = Field(None, alias="keepAlive")
    installer: str | None = None
    elevation: float | None = None
    splat_radius: float | None = Field(None, alias="splatRadius")

    # Features
    muted: bool | None = None
    transmission_authorized: bool | None = Field(None, alias="transmissionAuthorized")
    downlink_enabled: bool | None = Field(None, alias="downlinkEnabled")
    global_coverage_enable: bool | None = Field(None, alias="globalCoverageEnable")

    # Audit
    creation_time: int | None = Field(None, alias="creationTime")
    created_by: str | None = Field(None, alias="createdBy")
    last_edition_time: int | None = Field(None, alias="lastEditionTime")
    last_edited_by: str | None = Field(None, alias="lastEditedBy")

    # RF Configuration
    base_frequency: int | None = Field(None, alias="baseFrequency")
    downlink_center_frequency: int | None = Field(None, alias="downlinkCenterFrequency")
    macro_channel: int | None = Field(None, alias="macroChannel")
    tx_power_amplification: float | None = Field(None, alias="txPowerAmplification")
    protocol: int | None = None
    pre_amp1: int | None = Field(None, alias="preAmp1")
    pre_amp2: int | None = Field(None, alias="preAmp2")
    ram_log: int | None = Field(None, alias="RAMLog")
    wwan_mode: int | None = Field(None, alias="wwanMode")
    bit_rate: int | None = Field(None, alias="bitRate")

    # Equipment
    mast_equipment: int | None = Field(None, alias="mastEquipment")
    mast_equipment_description: str | None = Field(None, alias="mastEquipmentDescription")
    lna_by_pass: bool | None = Field(None, alias="lnaByPass")
    cavity_filter_version: int | None = Field(None, alias="cavityFilterVersion")
    cavity_filter_version_description: str | None = Field(None, alias="cavityFilterVersionDescription")

    # Antenna Properties
    antenna_gain: float | None = Field(None, alias="antennaGain")
    antenna_noise_figure: float | None = Field(None, alias="antennaNoiseFigure")
    antenna_insertion_loss: float | None = Field(None, alias="antennaInsertionLoss")
    antenna_max_admissible_power: float | None = Field(None, alias="antennaMaxAdmissiblePower")

    # RF Loss/Gain
    environment_loss: float | None = Field(None, alias="environmentLoss")
    cable_loss: float | None = Field(None, alias="cableLoss")
    gain_flag: bool | None = Field(None, alias="gainFlag")
    mast_equipment_gain: float | None = Field(None, alias="mastEquipmentGain")
    mast_equipment_noise_figure: float | None = Field(None, alias="mastEquipmentNoiseFigure")
    lna_insertion_loss: float | None = Field(None, alias="lnaInsertionLoss")
    cavity_filter_insertion_loss: float | None = Field(None, alias="cavityFilterInsertionLoss")
    tx_power_margin: float | None = Field(None, alias="txPowerMargin")

    # Optional
    antenna: dict | None = None
    monarch_beacon_enabled: bool | None = Field(None, alias="monarchBeaconEnabled")
    service_coverage: str | None = Field(None, alias="serviceCoverage")

    # Queue
    queue_in: int | None = Field(None, alias="queueIn")
    queue_out: int | None = Field(None, alias="queueOut")


class BaseStationUpdate(BaseModel):
    """Data for updating a base station.

    Only a subset of base station properties can be updated.
    All fields are optional (PUT only updates provided fields).
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str | None = None
    description: str | None = None
    base_station_alert_time: int | None = Field(None, alias="baseStationAlertTime")
    transmission_authorized: bool | None = Field(None, alias="transmissionAuthorized")
    installer: str | None = None
    global_coverage_enable: bool | None = Field(None, alias="globalCoverageEnable")
    elevation: float | None = None
    splat_radius: float | None = Field(None, alias="splatRadius")
    mast_equipment: int | None = Field(None, alias="mastEquipment")
    mast_equipment_description: str | None = Field(None, alias="mastEquipmentDescription")
    lna_by_pass: bool | None = Field(None, alias="lnaByPass")
    cavity_filter_version: int | None = Field(None, alias="cavityFilterVersion")
    cavity_filter_version_description: str | None = Field(None, alias="cavityFilterVersionDescription")
    environment_loss: float | None = Field(None, alias="environmentLoss")
    cable_loss: float | None = Field(None, alias="cableLoss")
    antenna_gain: float | None = Field(None, alias="antennaGain")
    antenna_noise_figure: float | None = Field(None, alias="antennaNoiseFigure")
    antenna_insertion_loss: float | None = Field(None, alias="antennaInsertionLoss")
    antenna_max_admissible_power: float | None = Field(None, alias="antennaMaxAdmissiblePower")
    service_coverage: str | None = Field(None, alias="serviceCoverage")
    antenna: dict | None = None
    monarch_beacon_enabled: bool | None = Field(None, alias="monarchBeaconEnabled")
