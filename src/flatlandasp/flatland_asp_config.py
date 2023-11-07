from functools import lru_cache
from typing import Any

import yaml


class FlatlandASPConfig(yaml.YAMLObject):
    asp_encodings_path: str
    asp_instances_path: str

    yaml_tag: str = '!config'
    yaml_loader = yaml.SafeLoader


@lru_cache
def get_config() -> FlatlandASPConfig:
    with open('config.yaml', 'r') as config_file:
        data: dict[str, Any] = yaml.safe_load(config_file)

        if "flatland_asp_config" not in data:
            raise (EOFError("Reached end of file before app_config was declared."))

        if not isinstance(data["flatland_asp_config"], FlatlandASPConfig):
            raise (TypeError("config.yaml is not correctly formatted"))

        return data["flatland_asp_config"]
