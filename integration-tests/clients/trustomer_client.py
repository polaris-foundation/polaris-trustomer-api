import requests
from environs import Env
from requests import Response


def _get_base_url() -> str:
    base_url: str = Env().str(
        "DHOS_TRUSTOMER_BASE_URL", "http://dhos-trustomer-api:5000"
    )
    return f"{base_url}/dhos/v1"


def get_trustomer_configuration(trustomer_header: str) -> Response:
    return requests.get(
        f"{_get_base_url()}/trustomer",
        timeout=15,
        headers={"X-Trustomer": trustomer_header},
    )


def get_trustomer_configuration_by_code(
    trustomer_header: str,
    trustomer: str,
    product: str = "gdm",
) -> Response:
    return requests.get(
        f"{_get_base_url()}/trustomer/{trustomer}",
        timeout=15,
        headers={"X-Trustomer": trustomer_header, "X-Product": product},
    )


def get_escalation_policy(trustomer_header: str, policy_name: str) -> Response:
    return requests.get(
        f"{_get_base_url()}/escalation_policy/{policy_name}",
        timeout=15,
        headers={"X-Trustomer": trustomer_header},
    )


def parse_patient_barcode(trustomer_header: str, patient_barcode: str) -> Response:
    return requests.post(
        f"{_get_base_url()}/parse_patient_barcode",
        timeout=15,
        headers={"X-Trustomer": trustomer_header},
        json={"barcode": patient_barcode},
    )
