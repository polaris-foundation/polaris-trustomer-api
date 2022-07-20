from typing import Any

from flask import Flask
from pytest_mock import MockFixture

from dhos_trustomer_api.blueprint_api import controller


class TestApi:
    def test_get_trustomer_returns_200(
        self,
        app: Flask,
        mocker: MockFixture,
        client: Any,
    ) -> None:
        expected = {"some": "content"}
        mocker.patch.object(controller, "get_trustomer_config", return_value=expected)
        response = client.get("/dhos/v1/trustomer", headers={"X-Trustomer": "dev"})
        assert response.status_code == 200
        assert response.json == expected

    def test_get_escalation_policy_content_returns_200(
        self,
        app: Flask,
        mocker: MockFixture,
        client: Any,
    ) -> None:
        expected = {"some": "content"}
        mocker.patch.object(
            controller,
            "get_escalation_policy_content",
            return_value=expected,
        )
        response = client.get(
            "/dhos/v1/escalation_policy/news2", headers={"X-Trustomer": "dev"}
        )
        assert response.status_code == 200
        assert response.json == expected

    def test_get_escalation_policy_content_unknown_score(
        self,
        app: Flask,
        mocker: MockFixture,
        client: Any,
    ) -> None:
        mock_get = mocker.patch.object(controller, "get_escalation_policy_content")
        mock_get.side_effects = KeyError()
        response = client.get(
            "/dhos/v1/escalation_policy/unknown",
            headers={"X-Trustomer": "dev"},
        )
        assert response.status_code == 400

    def test_parse_patient_barcode_invalid(
        self,
        app: Flask,
        mocker: MockFixture,
        client: Any,
    ) -> None:
        mock_parse = mocker.patch.object(controller, "parse_patient_barcode")
        mock_parse.side_effects = ValueError()
        response = client.post(
            "/dhos/v1/parse_patient_barcode",
            json={"barcode": "something"},
            headers={"X-Trustomer": "dev"},
        )
        assert response.status_code == 400

    def test_parse_patient_barcode_no_body(self, app: Flask, client: Any) -> None:
        response = client.post(
            "/dhos/v1/parse_patient_barcode", headers={"X-Trustomer": "dev"}
        )
        assert response.status_code == 400

    def test_parse_patient_barcode_no_barcode(self, app: Flask, client: Any) -> None:
        response = client.post(
            "/dhos/v1/parse_patient_barcode",
            json={"barcode": None},
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 400

    def test_parse_patient_barcode_wrong_fields(self, app: Flask, client: Any) -> None:
        response = client.post(
            "/dhos/v1/parse_patient_barcode",
            json={"not_barcode": "something", "extra": 42},
            headers={"X-Trustomer": "dev"},
        )
        assert response.status_code == 400

    def test_parse_patient_barcode_success(
        self,
        app: Flask,
        mocker: MockFixture,
        client: Any,
    ) -> None:
        expected = {"groups": {"key": "value"}}
        mocker.patch.object(controller, "parse_patient_barcode", return_value=expected)
        response = client.post(
            "/dhos/v1/parse_patient_barcode",
            json={"barcode": "something"},
            headers={"X-Trustomer": "dev"},
        )
        assert response.status_code == 200
        assert response.json == expected

    def test_get_trustomer_by_code(
        self,
        app: Flask,
        mocker: MockFixture,
        client: Any,
    ) -> None:
        expected = {"some": "content"}
        mocker.patch.object(controller, "get_trustomer_config", return_value=expected)
        response = client.get(
            "/dhos/v1/trustomer/dev", headers={"X-Trustomer": "dev", "X-Product": "gdm"}
        )
        assert response.status_code == 200
        assert response.json == expected

    def test_get_trustomer_by_code_forbidden(
        self,
        app: Flask,
        client: Any,
    ) -> None:
        response = client.get(
            "/dhos/v1/trustomer/trust1",
            headers={"X-Trustomer": "trust2", "X-Product": "gdm"},
        )
        assert response.status_code == 403

    def test_get_trustomer_by_code_headers_missing(
        self,
        app: Flask,
        client: Any,
    ) -> None:
        response = client.get(
            "/dhos/v1/trustomer/trust1",
        )
        assert response.status_code == 400
