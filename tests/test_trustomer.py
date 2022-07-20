import pytest

from dhos_trustomer_api.blueprint_api import trustomer


class TestTrustomer:
    def test_load_trustomer_config_success(self) -> None:
        trustomer.trustomer_config = {}
        trustomer.load_trustomer_config("./trustomer-config-dummy")
        assert trustomer.trustomer_config.keys() == {
            "dev",
            "usdev",
            "staging",
        }

    def test_load_trustomer_config_not_dir(self) -> None:
        with pytest.raises(EnvironmentError):
            trustomer.load_trustomer_config("./fake")

    def test_load_trustomer_config_invalid(self) -> None:
        trustomer.trustomer_config = {}
        with pytest.raises(EnvironmentError):
            trustomer.load_trustomer_config("./tests/trustomer-config-invalid")
