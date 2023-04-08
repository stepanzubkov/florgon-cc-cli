"""
    Services for working with user config.
"""
from typing import Any
import toml

from florgon_cc_cli import config


def save_value_to_config(key: str, value: Any) -> None:
    """
    Saves value to user config by key.
    :param str key: key for value.
    :param Any value: value to save.
    :rtype: None
    """
    config.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    config.CONFIG_FILE.touch(exist_ok=True)

    with open(config.CONFIG_FILE, "r") as f:
        user_config = toml.load(f)

    user_config[key] = value
    with open(config.CONFIG_FILE, "w") as f:
        toml.dump(user_config, f)


def get_value_from_config(key: str) -> Any:
    """
    Returns value from config by key.
    :param str key: key for value
    :rtype: Any
    """
    config.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    config.CONFIG_FILE.touch(exist_ok=True)

    with open(config.CONFIG_FILE, "r") as f:
        user_config = toml.load(f)

    return user_config.get(key)
