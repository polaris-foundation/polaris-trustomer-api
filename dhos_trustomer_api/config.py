from typing import Optional

from environs import Env
from flask import Flask


class Configuration:
    env = Env()
    COUNTLY_APP_KEY_MOBILE_NONPROD_OVERRIDE: Optional[str] = env.str(
        "COUNTLY_APP_KEY_MOBILE_NONPROD_OVERRIDE", None
    )
    COUNTLY_APP_KEY_WEBAPP_NONPROD_OVERRIDE: Optional[str] = env.str(
        "COUNTLY_APP_KEY_WEBAPP_NONPROD_OVERRIDE", None
    )
    TRUSTOMER_CONFIG_MOUNT = env.str("TRUSTOMER_CONFIG_MOUNT", "/trustomer-config")


def apply_config(app: Flask) -> None:
    app.config.from_object(Configuration)
