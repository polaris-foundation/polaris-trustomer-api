from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class MeasurementSystem(str, Enum):
    METRIC = "metric"
    IMPERIAL = "imperial"


class AlertsSystem(str, Enum):
    COUNTS = "counts"
    PERCENTAGES = "percentages"


class BgUnit(str, Enum):
    MMOL_L = "mmol/L"
    MG_DL = "mg/dL"


class BgThreshold(BaseModel):
    high: float
    low: float


class BgThresholdSet(BaseModel):
    before_breakfast: BgThreshold = Field(alias="BEFORE-BREAKFAST")
    after_breakfast: BgThreshold = Field(alias="AFTER-BREAKFAST")
    before_lunch: BgThreshold = Field(alias="BEFORE-LUNCH")
    after_lunch: BgThreshold = Field(alias="AFTER-LUNCH")
    before_dinner: BgThreshold = Field(alias="BEFORE-DINNER")
    after_dinner: BgThreshold = Field(alias="AFTER-DINNER")
    other: BgThreshold = Field(alias="OTHER")


class BgThresholdSuperset(BaseModel):
    type1: BgThresholdSet
    type2: BgThresholdSet
    other: BgThresholdSet


class PhoneNumber(BaseModel):
    label: str
    number: str


class JobTitle(BaseModel):
    title: str
    value: str


class NurseConcern(BaseModel):
    code: str
    name: str
    text: str


class OxygenMask(BaseModel):
    code: str
    id: str
    name: str


class BarcodeFormat(BaseModel):
    can_create_patient: bool
    format: str


class GdmAppsLegal(BaseModel):
    gdm_terms_of_use_content: str
    gdm_terms_of_use_version: int
    gdm_patient_notice_content: str
    gdm_patient_notice_version: int
    gdm_clinician_terms_content: str
    gdm_clinician_terms_version: int


class DbmAppsLegal(BaseModel):
    terms_of_use_content: str
    terms_of_use_version: int
    patient_notice_content: str
    patient_notice_version: int
    clinician_terms_content: str
    clinician_terms_version: int


class EscalationPolicy(BaseModel):
    high_monitoring: str
    low_medium_monitoring: str
    low_monitoring: str
    medium_monitoring: str
    routine_monitoring: str


class EwsConfig(BaseModel):
    escalation_policy: EscalationPolicy
    high_severity_interval_hours: float
    low_medium_severity_interval_hours: float
    low_severity_interval_hours: float
    medium_severity_interval_hours: float
    zero_severity_interval_hours: float


class GdmConfig(BaseModel):
    alerts_snooze_duration_days: int
    alerts_system: AlertsSystem
    article_tags: list[str]
    blood_glucose_thresholds_mmoll: BgThresholdSet
    blood_glucose_units: BgUnit
    contact_phone_numbers: list[PhoneNumber]
    countly_app_url: Optional[str]
    countly_app_key_mobile: Optional[str]
    countly_app_key_webapp: Optional[str]
    medication_tags: list[str]
    gdm_desktop_timeout_minutes: int
    graph_thresholds_mmoll: BgThreshold
    use_bff_for_readings_post: bool
    use_diabetes_category_pre_gdm: bool
    use_sms_content_override: bool
    use_syne_data_extract: bool
    use_syne_predictions: bool
    gdm_apps_legal: GdmAppsLegal


class DbmConfig(BaseModel):
    article_tags: list[str]
    blood_glucose_thresholds_mmoll: BgThresholdSuperset
    blood_glucose_units: BgUnit
    contact_phone_numbers: list[PhoneNumber]
    countly_app_url: Optional[str]
    countly_app_key_mobile: Optional[str]
    countly_app_key_webapp: Optional[str]
    desktop_timeout_minutes: int
    graph_thresholds_mmoll: BgThreshold
    medication_tags: list[str]
    legal: DbmAppsLegal


class Hl7Config(BaseModel):
    outgoing_processing_id: str
    outgoing_receiving_application: str
    outgoing_receiving_facility: str
    outgoing_sending_application: str
    outgoing_sending_facility: str
    outgoing_timestamp_format: str


class SendConfig(BaseModel):
    allow_take_obs_in_desktop: bool
    generate_oru_messages: bool
    job_titles: list[JobTitle]
    max_retrospective_obs_period_hours: int
    news2: EwsConfig
    nurse_concern: list[NurseConcern]
    nurse_concerns: list[str]
    oxygen_masks: list[OxygenMask]
    patient_barcode_format: list[BarcodeFormat]
    post_discharge_display_time_hours: int
    send_desktop_timeout_minutes: int
    send_entry_timeout_minutes: int
    send_terms_content: str
    send_terms_version: int
    meows: Optional[EwsConfig]


class TrustomerConfigSchema(BaseModel):
    uuid: str
    name: str
    created: str
    modified: str
    gdm_phone_ward: str
    gdm_phone_midwife: str
    measurement_system: MeasurementSystem
    gdm_terms_version: int
    gdm_terms_content: str
    gdm_clinician_terms_version: int
    gdm_clinician_terms_content: str
    gdm_config: GdmConfig
    dbm_config: DbmConfig
    hl7_config: Hl7Config
    send_config: SendConfig
