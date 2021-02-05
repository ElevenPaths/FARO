import importlib
import logging
import os
from abc import ABC, abstractmethod

import yaml

logger = logging.getLogger(__name__)


def get_supported_languages(path):
    with os.scandir(path) as files:
        supported_languages = [file.name for file in files if file.is_dir()]
    return supported_languages


def load_module(plugin_name):
    try:
        plugin = importlib.import_module(plugin_name)
        return plugin
    except Exception as e:
        logger.error(f"[load_plugin] {e}")


def load_config(path, config_path):
    commons_yaml = os.path.join(path, config_path)
    with open(commons_yaml, "r", encoding='utf8') as f_stream:
        commons_config = yaml.load(f_stream, Loader=yaml.FullLoader)
    return commons_config


def get_plugins_list(path):
    with os.scandir(path) as files:
        plugins = [file.name for file in files if file.is_dir() and not file.name.startswith("__")]
    return plugins


class BasePlugin(ABC):
    def __init__(self, text, lang):
        self.text = text
        self.lang = lang

    @abstractmethod
    def run(self):
        pass
