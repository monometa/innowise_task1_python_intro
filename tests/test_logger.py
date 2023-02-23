from modules.logs.set_logging_conf import set_app_logger, get_config_file_path
import yaml
from logging import Logger


def test_get_config_path_file_return_existsing_file():
    assert get_config_file_path().is_file()


def test_if_yml_config_is_not_empty():
    with open(get_config_file_path(), "r") as y_file:
        content = yaml.safe_load(y_file) or {}
    assert content


def test_get_config_path_return_yaml_or_yml_file():
    str(get_config_file_path()).lower().endswith(("yaml", "yml"))


def test_set_logger_default():
    assert isinstance(set_app_logger(config_path=get_config_file_path()), Logger)
