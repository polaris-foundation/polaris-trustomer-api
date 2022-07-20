from behave import step
from behave.runner import Context
from clients.trustomer_client import get_escalation_policy
from requests import Response


@step("I get {name} escalation policy")
def assert_escalation_policy(context: Context, name: str) -> None:
    response: Response = get_escalation_policy(
        trustomer_header=context.trustomer_header,
        policy_name=name,
    )
    if name == "non-existent":
        assert response.status_code == 400
        context.escalation_policy = None
    else:
        response.raise_for_status()
        context.escalation_policy = response.json()


@step("I see it contains the following configuration options")
def assert_configuration_options(context: Context) -> None:
    for option in context.table:
        assert context.escalation_policy[option["name"]] == option["value"]


@step("I see it contains no configuration options")
def assert_no_configuration_options(context: Context) -> None:
    assert not context.escalation_policy
