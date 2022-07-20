import click
from flask import Flask
from flask_batteries_included.helpers.apispec import generate_openapi_spec

from dhos_trustomer_api.blueprint_api import api_blueprint
from dhos_trustomer_api.models.api_spec import dhos_trustomer_api_spec


def add_cli_command(app: Flask) -> None:
    @app.cli.command("create-openapi")
    @click.argument("output", type=click.Path())
    def create_api(output: str) -> None:
        generate_openapi_spec(dhos_trustomer_api_spec, output, api_blueprint)
