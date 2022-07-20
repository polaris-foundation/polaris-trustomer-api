import json
from pathlib import Path

from behave import given, step
from behave.runner import Context
from clients import trustomer_client
from requests import Response


@given("I have trustomer headers for {trustomer}")
def set_trustomer_headers(context: Context, trustomer: str) -> None:
    context.trustomer_header = trustomer


@given("I have no trustomer headers")
def set_trustomer_headers_none(context: Context) -> None:
    context.trustomer_header = None


@step("I get trustomer configuration")
def trustomer_config(context: Context) -> None:
    response: Response = trustomer_client.get_trustomer_configuration(
        trustomer_header=context.trustomer_header
    )
    context.trustomer_response = response


@step("I get trustomer configuration for {trustomer}")
def trustomer_config_by_code(context: Context, trustomer: str) -> None:
    response: Response = trustomer_client.get_trustomer_configuration_by_code(
        trustomer_header=context.trustomer_header,
        trustomer=trustomer,
    )
    context.trustomer_response = response


@step("I get an error")
def check_auth_error(context: Context) -> None:
    assert 400 <= context.trustomer_response.status_code < 500


@step("I see it matches the trustomer config file")
def config_matches_trustomer_config_file(context: Context) -> None:
    dev_json_file = Path("/trustomer-config") / "DEV" / "content.json"
    expected = json.loads(dev_json_file.read_text())
    assert context.trustomer_response.status_code == 200
    assert context.trustomer_response.json() == expected
