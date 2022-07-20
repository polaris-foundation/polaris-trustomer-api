from typing import Dict

import pytest
from flask import current_app
from pytest_mock import MockFixture

from dhos_trustomer_api.blueprint_api import controller, trustomer


@pytest.mark.usefixtures("app")
class TestController:
    def test_get_escalation_policy_content_success(
        self, mocker: MockFixture, trustomer_config: Dict
    ) -> None:
        system = "news2"
        mocker.patch.dict(trustomer.trustomer_config, {"dev": trustomer_config})
        actual = controller.get_escalation_policy_content(
            trustomer_code="dev", name=system
        )
        assert actual == trustomer_config["send_config"][system]["escalation_policy"]

    def test_get_escalation_policy_content_unknown(
        self, mocker: MockFixture, trustomer_config: dict
    ) -> None:
        mocker.patch.dict(trustomer.trustomer_config, {"dev": trustomer_config})
        with pytest.raises(KeyError):
            controller.get_escalation_policy_content(
                trustomer_code="dev", name="missing_name"
            )

    def test_parse_patient_barcode_ouh_success(
        self, mocker: MockFixture, trustomer_config: Dict
    ) -> None:
        trustomer_config["send_config"]["patient_barcode_format"] = [
            {
                "format": r"^(?:.*?)([\|±])(?<mrn>\d+)([\|±])(?<nhs>\d*)([\|±])(?<lastname>.+?)([\|±])(?<firstname>.+?)([\|±])(?<dob>(?:0[1-9]|1\d|2\d|3[01])\/(?:0[1-9]|1[0-2])\/(?:19|20)\d{2})([\|±])(?<sex>F|M|U)$"
            }
        ]
        mocker.patch.dict(trustomer.trustomer_config, {"dev": trustomer_config})
        result = controller.parse_patient_barcode(
            trustomer_code="dev", barcode="W1|615592|9998458646|Mclean|Amy|23/12/1981|F"
        )
        expected = {
            "groups": {
                "dob": "23/12/1981",
                "firstname": "Amy",
                "lastname": "Mclean",
                "mrn": "615592",
                "nhs": "9998458646",
                "sex": "F",
            }
        }
        assert result == expected

    def test_parse_patient_barcode_ouh_invalid(
        self, mocker: MockFixture, trustomer_config: Dict
    ) -> None:
        trustomer_config["send_config"]["patient_barcode_format"] = [
            {
                "format": r"^(?:.*?)([\|±])(?<mrn>\d+)([\|±])(?<nhs>\d*)([\|±])(?<lastname>.+?)([\|±])(?<firstname>.+?)([\|±])(?<dob>(?:0[1-9]|1\d|2\d|3[01])\/(?:0[1-9]|1[0-2])\/(?:19|20)\d{2})([\|±])(?<sex>F|M|U)$"
            }
        ]
        mocker.patch.dict(trustomer.trustomer_config, {"dev": trustomer_config})
        with pytest.raises(ValueError):
            controller.parse_patient_barcode(
                trustomer_code="dev", barcode="this_is_wrong"
            )

    def test_parse_patient_barcode_swft_success(
        self, mocker: MockFixture, trustomer_config: Dict
    ) -> None:
        trustomer_config["send_config"]["patient_barcode_format"] = [
            {
                "format": r"^80185050898(?<nhs>\d+)\d91RJC,(?<mrn>\d+),50552303,93(?<lastname>[^,]+),(?<firstname>[^,]+),(?<dob>\d{1,2}-[a-zA-Z]+-\d+),$"
            }
        ]
        mocker.patch.dict(trustomer.trustomer_config, {"dev": trustomer_config})
        result = controller.parse_patient_barcode(
            trustomer_code="dev",
            barcode="801850508981009690538391RJC,949724,50552303,93JORDAN,Dwayne,29-Nov-1949,",
        )
        expected = {
            "groups": {
                "dob": "29-Nov-1949",
                "firstname": "Dwayne",
                "lastname": "JORDAN",
                "mrn": "949724",
                "nhs": "1009690538",
            }
        }
        assert result == expected

    def test_parse_patient_barcode_swft_invalid(
        self, mocker: MockFixture, trustomer_config: Dict
    ) -> None:
        trustomer_config["send_config"]["patient_barcode_format"] = [
            {
                "format": r"^80185050898(?<nhs>\d+)\d91RJC,(?<mrn>\d+),50552303,93(?<lastname>[^,]+),(?<firstname>[^,]+),(?<dob>\d{1,2}-[a-zA-Z]+-\d+),$"
            }
        ]
        mocker.patch.dict(trustomer.trustomer_config, {"dev": trustomer_config})
        with pytest.raises(ValueError):
            controller.parse_patient_barcode(
                trustomer_code="dev", barcode="this_is_wrong"
            )

    def test_parse_patient_barcode_1d_success(
        self, mocker: MockFixture, trustomer_config: Dict
    ) -> None:
        trustomer_config["send_config"]["patient_barcode_format"] = [
            {"format": "^(?<mrn>[a-zA-Z0-9]+)$"}
        ]
        mocker.patch.dict(trustomer.trustomer_config, {"dev": trustomer_config})
        result = controller.parse_patient_barcode(
            trustomer_code="dev", barcode="615592"
        )
        expected = {"groups": {"mrn": "615592"}}
        assert result == expected

    def test_parse_patient_barcode_1d_invalid(
        self, mocker: MockFixture, trustomer_config: Dict
    ) -> None:
        trustomer_config["send_config"]["patient_barcode_format"] = [
            {"format": "^(?<mrn>[a-zA-Z0-9]+)$"}
        ]
        mocker.patch.dict(trustomer.trustomer_config, {"dev": trustomer_config})
        with pytest.raises(ValueError):
            controller.parse_patient_barcode(trustomer_code="dev", barcode="615592@_")

    @pytest.mark.parametrize(
        ("barcode", "expected"),
        [
            (
                "W1|615592|9998458646|Mclean|Amy|23/12/1981|F",
                {
                    "groups": {
                        "dob": "23/12/1981",
                        "firstname": "Amy",
                        "lastname": "Mclean",
                        "mrn": "615592",
                        "nhs": "9998458646",
                        "sex": "F",
                    }
                },
            ),
            (
                "801850508981009690538391RJC,949724,50552303,93JORDAN,Dwayne,29-Nov-1949,",
                {
                    "groups": {
                        "dob": "29-Nov-1949",
                        "firstname": "Dwayne",
                        "lastname": "JORDAN",
                        "mrn": "949724",
                        "nhs": "1009690538",
                    }
                },
            ),
            ("615592", {"groups": {"mrn": "615592"}}),
        ],
    )
    def test_parse_patient_barcode_multiple_options(
        self, mocker: MockFixture, trustomer_config: dict, barcode: str, expected: Dict
    ) -> None:
        mocker.patch.dict(trustomer.trustomer_config, {"dev": trustomer_config})
        result = controller.parse_patient_barcode(trustomer_code="dev", barcode=barcode)
        assert result == expected

    def test_get_trustomer_config_from_files(self) -> None:
        dev_config = controller.get_trustomer_config(trustomer_code="dev")
        assert dev_config["uuid"] == "2c4f1d24-2952-4d4e-b1d1-3637e33cc161"

    def test_get_trustomer_config_from_mock(
        self, mocker: MockFixture, trustomer_config: Dict
    ) -> None:
        mocker.patch.dict(trustomer.trustomer_config, {"dev": trustomer_config})
        result = controller.get_trustomer_config(trustomer_code="dev")
        assert result == trustomer_config

    @pytest.mark.parametrize(
        ["is_prod", "override_set", "override_expected"],
        [
            (True, False, False),
            (True, True, False),
            (False, False, False),
            (False, True, True),
        ],
    )
    def test_trustomer_config_countly_nonprod_override(
        self,
        mocker: MockFixture,
        trustomer_config: dict,
        is_prod: bool,
        override_set: bool,
        override_expected: bool,
    ) -> None:
        mobile_original_key = "12345"
        webapp_original_key = "ABCDE"
        mobile_override_key = "98765"
        webapp_override_key = "ZYXWV"
        if override_set:
            current_app.config[
                "COUNTLY_APP_KEY_MOBILE_NONPROD_OVERRIDE"
            ] = mobile_override_key
            current_app.config[
                "COUNTLY_APP_KEY_WEBAPP_NONPROD_OVERRIDE"
            ] = webapp_override_key
        mocker.patch.object(
            controller, "is_production_environment", return_value=is_prod
        )
        mocker.patch.dict(trustomer.trustomer_config, {"dev": trustomer_config})
        result = controller.get_trustomer_config(trustomer_code="dev")
        actual_key_mobile: str = result["gdm_config"]["countly_app_key_mobile"]
        actual_key_webapp: str = result["gdm_config"]["countly_app_key_webapp"]
        if override_expected:
            assert actual_key_mobile == mobile_override_key
            assert actual_key_webapp == webapp_override_key
        else:
            assert actual_key_mobile == mobile_original_key
            assert actual_key_webapp == webapp_original_key

    def test_get_escalation_policy(self) -> None:
        staging_news2_policy = controller.get_escalation_policy_content(
            trustomer_code="staging", name="news2"
        )
        assert staging_news2_policy["high_monitoring"].startswith(
            "<p>Registered nurse to immediately inform"
        )

    def test_parse_patient_barcode(self, trustomer_config: Dict) -> None:
        result = controller.parse_patient_barcode(
            trustomer_code="dev", barcode="615592"
        )
        assert result == {"groups": {"mrn": "615592"}}
