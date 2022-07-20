import json
from pathlib import Path

from pydantic import ValidationError
from she_logging import logger

from dhos_trustomer_api.blueprint_api.schema import TrustomerConfigSchema

trustomer_config = {}


def load_trustomer_config(parent_path: str) -> None:
    """
    Loads trustomer config from a directory into memory. Expects the directory at `parent_path` to have the following
    structure:
    -> <trustomer 1>
        -> content.json
    -> <trustomer 2>
        -> content.json
    -> <trustomer 3>
        -> content.json
    """
    parent_dir = Path(parent_path)
    if not parent_dir.exists() or not parent_dir.is_dir():
        raise EnvironmentError(
            f"Trustomer config directory {parent_path} does not exist"
        )
    for trustomer in parent_dir.iterdir():
        if not trustomer.is_dir():
            continue
        config_file = trustomer / "content.json"
        contents = json.loads(config_file.read_text())
        try:
            TrustomerConfigSchema.parse_obj(contents)
        except ValidationError:
            logger.exception("Error validating trustomer file '%s'", config_file)
            raise EnvironmentError(f"Invalid trustomer file '{config_file}'")
        trustomer_config[trustomer.name.lower()] = contents
    n_trustomers = len(trustomer_config.keys())
    if n_trustomers == 0:
        raise EnvironmentError(f"No trustomer config found in directory {parent_path}")
    logger.info("Loaded config for %d trustomers", n_trustomers)
