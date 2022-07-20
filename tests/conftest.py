from typing import Any, Dict, Generator

import pytest
from flask import Flask


@pytest.fixture
def app_environment() -> str:
    return "DEVELOPMENT"


@pytest.fixture()
def app(monkeypatch: Any, app_environment: str) -> Generator[Flask, None, None]:
    """Fixture that creates app for testing"""
    from dhos_trustomer_api.app import create_app

    yield create_app(testing=True)


@pytest.fixture
def app_context(app: Flask) -> Generator[None, None, None]:
    with app.app_context():
        yield


@pytest.fixture
def trustomer_config() -> Dict:
    """Trustomer configuration"""
    return {
        "gdm_config": {
            "countly_app_key_mobile": "12345",
            "countly_app_key_webapp": "ABCDE",
        },
        "send_config": {
            "news2": {
                "zero_severity_interval_hours": 12,
                "low_severity_interval_hours": 4,
                "low_medium_severity_interval_hours": 1,
                "medium_severity_interval_hours": 1,
                "high_severity_interval_hours": 0,
                "escalation_policy": {
                    "routine_monitoring": "<p>Continue routine NEWS monitoring</p>",
                    "low_monitoring": "<p>Inform registered nurse, who must assess the patient</p><p>Registered nurse decides whether increased frequency of monitoring and/or escalation of care is required</p>",
                    "low_medium_monitoring": "<p>Registered nurse to inform medical team caring for the patient, who will review and decide whether escalation of care is necessary</p>",
                    "medium_monitoring": "<p>Registered nurse to immediately inform the medical team caring for the patient</p><p>Registered nurse to request urgent assessment by a clinician or team with core competencies in the care of acutely ill patients</p><p>Provide clinical care in an environment with monitoring facilities</p>",
                    "high_monitoring": "<p>Registered nurse to immediately inform the medical team caring for the patient – this should be at least at specialist registrar level</p><p>Emergency assessment by a team with critical care competencies, including practitioner(s) with advanced airway management skills</p><p>Consider transfer of care to a level 2 or 3 clinical care facility, ie higher-dependency unit or ICU</p><p>Clinical care in an environment with monitoring facilities</p>",
                },
            },
            "patient_barcode_format": [
                {
                    "format": r"^(?:.*?)([\|±])(?<mrn>\d+)([\|±])(?<nhs>\d*)([\|±])(?<lastname>.+?)([\|±])(?<firstname>.+?)([\|±])(?<dob>(?:0[1-9]|1\d|2\d|3[01])\/(?:0[1-9]|1[0-2])\/(?:19|20)\d{2})([\|±])(?<sex>F|M|U)$"
                },
                {
                    "format": r"^80185050898(?<nhs>\d+)\d91RJC,(?<mrn>\d+),50552303,93(?<lastname>[^,]+),(?<firstname>[^,]+),(?<dob>\d{1,2}-[a-zA-Z]+-\d+),$"
                },
                {"format": "^(?<mrn>[a-zA-Z0-9]+)$"},
            ],
        },
    }
