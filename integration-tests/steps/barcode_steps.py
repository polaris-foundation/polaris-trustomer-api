from json import loads
from pathlib import Path

from behave import step
from behave.runner import Context
from clients.trustomer_client import parse_patient_barcode
from requests import Response


@step("I parse patient barcode in {format_name} format")
def call_parse_patient_barcode(context: Context, format_name: str) -> None:
    barcode_content: str = Path("./resources", f"barcode_{format_name}.txt").read_text()
    response: Response = parse_patient_barcode(
        trustomer_header=context.trustomer_header,
        patient_barcode=barcode_content,
    )

    if format_name == "unsupported":
        assert response.status_code == 400
        context.decoded_barcode = None
    else:
        response.raise_for_status()
        context.decoded_barcode = response.json()


@step("I get the barcode information as defined by the {format_name}")
def assert_barcode_content(context: Context, format_name: str) -> None:
    expected: str = Path(
        "./resources", f"barcode_decoded_{format_name}.json"
    ).read_text()
    assert context.decoded_barcode == loads(expected)


@step("I get no barcode information")
def assert_no_barcode_decoded(context: Context) -> None:
    assert not context.decoded_barcode
