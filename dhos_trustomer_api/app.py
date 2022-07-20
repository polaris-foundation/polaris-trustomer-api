from pathlib import Path

import connexion
from connexion import FlaskApp
from flask import Flask
from flask_batteries_included import augment_app as fbi_augment_app
from flask_batteries_included.config import is_not_production_environment

from dhos_trustomer_api.blueprint_api import api_blueprint
from dhos_trustomer_api.blueprint_api.trustomer import load_trustomer_config
from dhos_trustomer_api.config import apply_config
from dhos_trustomer_api.helper.cli import add_cli_command


def create_app(testing: bool = False) -> Flask:
    # Create a Flask app
    openapi_dir: Path = Path(__file__).parent / "openapi"
    connexion_app: FlaskApp = connexion.App(
        __name__,
        specification_dir=openapi_dir,
        options={"swagger_ui": is_not_production_environment()},
    )
    connexion_app.add_api("openapi.yaml", strict_validation=True)
    app: Flask = fbi_augment_app(app=connexion_app.app, use_jwt=False, testing=testing)

    apply_config(app)

    # Add the API blueprint
    app.register_blueprint(api_blueprint, url_prefix="/dhos/v1")

    add_cli_command(app)

    # Load trustomer config from files.
    app.logger.info("Loading trustomer config")
    load_trustomer_config(parent_path=app.config["TRUSTOMER_CONFIG_MOUNT"])

    return app
