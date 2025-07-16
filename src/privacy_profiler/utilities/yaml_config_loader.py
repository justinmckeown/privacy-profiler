import yaml
import argparse
from typing import Optional


def load_yaml_config(path: str) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}


def merge_configs(cli_args: argparse.Namespace, yaml_config: Optional[dict]) -> argparse.Namespace:
    final = vars(cli_args).copy()

    if yaml_config:
        for key, value in yaml_config.items():
            if final.get(key) in [None, [], False]:
                final[key] = value

    # Normalize: unify input → input_path if present
    if final.get("input") and not final.get("input_path"):
        final["input_path"] = final["input"]

    return argparse.Namespace(**final)
