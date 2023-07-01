"""
    Services for working with user config.
"""
from typing import Any, Dict, Optional
import toml

import click

from florgon_cc_cli import config


def get_access_token() -> Optional[str]:
    """
    Return access_token from user config or
    returns None if passed --anonymous flag.
    :returns: access token
    :rtype: Optional[str]
    """
    ctx = click.get_current_context()
    return None if ctx.obj["ANONYMOUS"] else get_value_from_config("access_token")


def save_value_to_config(key: str, value: Any) -> None:
    """
    Saves value to user config by key.
    :param str key: key for value.
    :param Any value: value to save.
    :rtype: None
    """
    create_config_file()
    user_config = deserialize_config()

    user_config[key] = value
    with open(config.CONFIG_FILE, "w") as f:
        toml.dump(user_config, f)


def get_value_from_config(key: str) -> Any:
    """
    Returns value from config by key.
    NOTE: Do not use this function to get access token, use get_access_token() instead!
    :param str key: key for value
    :rtype: Any
    """
    create_config_file()
    user_config = deserialize_config()

    return user_config.get(key)


def delete_value_from_config(key: str) -> None:
    """
    Deletes value from config by key.
    :param str key: key for value
    :rtype: None
    """
    create_config_file()
    user_config = deserialize_config()

    if key in user_config:
        user_config.pop(key)

    with open(config.CONFIG_FILE, "w") as f:
        toml.dump(user_config, f)


def deserialize_config() -> Dict[str, Any]:
    """
    Deserializes config and returns dict.
    :rtype: Dict[str, Any]
    :return: user config
    """
    with open(config.CONFIG_FILE, "r") as f:
        return toml.load(f)


def create_config_file() -> None:
    """
    Creates empty config dir and config file.
    :rtype: None
    """
    config.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    config.CONFIG_FILE.touch(exist_ok=True)
