import re
from typing import List, Optional

from flask import current_app
from flask_batteries_included.config import is_production_environment
from she_logging import logger

from dhos_trustomer_api.blueprint_api.trustomer import trustomer_config


def get_trustomer_config(trustomer_code: str) -> dict:
    config: dict = trustomer_config[trustomer_code]
    _override_countly_config(config)
    return config


def get_escalation_policy_content(trustomer_code: str, name: str) -> dict:
    base: dict = get_trustomer_config(trustomer_code)
    score_system = base["send_config"].get(name)
    if not score_system:
        raise KeyError(f"score system {name} does not exist")
    return score_system["escalation_policy"]


def parse_patient_barcode(trustomer_code: str, barcode: str) -> dict:
    base: dict = get_trustomer_config(trustomer_code)
    barcode_formats: List[dict] = base["send_config"]["patient_barcode_format"]
    # Loop through regex list and accept first match
    for barcode_format in barcode_formats:
        # Python needs a "P" for named capture groups to work...
        regex: str = barcode_format["format"].replace("(?<", "(?P<")
        match = re.search(regex, barcode)
        if match is None:
            continue
        return {"groups": {k: v for k, v in match.groupdict().items() if v is not None}}
    raise ValueError("Could not parse barcode")


def _override_countly_config(config: dict) -> None:
    if not is_production_environment():
        # Override the Countly app keys if (all of):
        # 1) They are set
        # 2) The overrides are set
        # 3) We're in a non-prod environment
        countly_app_key_mobile: Optional[str] = config["gdm_config"].get(
            "countly_app_key_mobile", None
        )
        countly_app_key_webapp: Optional[str] = config["gdm_config"].get(
            "countly_app_key_webapp", None
        )
        nonprod_mobile_override: Optional[str] = current_app.config[
            "COUNTLY_APP_KEY_MOBILE_NONPROD_OVERRIDE"
        ]
        nonprod_webapp_override: Optional[str] = current_app.config[
            "COUNTLY_APP_KEY_WEBAPP_NONPROD_OVERRIDE"
        ]
        if countly_app_key_mobile and nonprod_mobile_override:
            logger.debug("Overriding Countly mobile app key to non-prod instance")
            config["gdm_config"]["countly_app_key_mobile"] = nonprod_mobile_override
        if countly_app_key_webapp and nonprod_webapp_override:
            logger.debug("Overriding Countly webapp key to non-prod instance")
            config["gdm_config"]["countly_app_key_webapp"] = nonprod_webapp_override
