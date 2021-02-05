#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ast
from pathlib import Path

from conf import config
from logger import logger
from utils.base_plugin import load_module, get_plugins_list

script_name = Path(__file__).name
faro_logger = logger.Logger(logger_name=script_name, file_name=config.LOG_FILE_NAME, logging_level=config.LOG_LEVEL)


class Orchestrator:
    def __init__(self, conf):
        self.config = conf
        self.results = {}
        self.plugins_path = Path(__file__).parent
        self.plugin_list = get_plugins_list(self.plugins_path)

    def _load_plugin(self, exec_plugin, content):
        if exec_plugin in self.plugin_list:
            module = self.plugins_path.name + "." + exec_plugin + ".entrypoint"
            return load_module(module).PluginEntrypoint(content, self.config["lang"])
        else:
            faro_logger.error(script_name,
                              self._load_plugin.__name__,
                              f"Plugin {exec_plugin} not found.")
            return None

    def _update_results(self, detection_results):
        if not detection_results == {}:
            ent_key = list(detection_results)[0]
            if ent_key in self.results:
                self.results[ent_key].update(detection_results[ent_key])
            else:
                self.results.update(detection_results)

    def _select_plugins_to_run(self):
        run_all = self.config["plugins"]["all"]
        return self.plugin_list if run_all \
            else self.config["plugins"]["available_list"]

    def run_plugins(self, content):
        content = ast.literal_eval(content)

        execute_plugins = self._select_plugins_to_run()

        for exec_plugin in execute_plugins:
            plugin = self._load_plugin(exec_plugin, content)
            if plugin:
                faro_logger.debug(script_name,
                                  self.run_plugins.__name__,
                                  f"Executing plugin {exec_plugin}.")
                try:
                    plugin_results = plugin.run()
                    self._update_results(plugin_results)
                except Exception as e:
                    message = "Error running plugin %s due to exception %s" % (exec_plugin, e)
                    faro_logger.error(script_name, self.run_plugins.__name__, message)

        return self.results
