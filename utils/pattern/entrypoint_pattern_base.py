#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from abc import abstractmethod

from utils.base_plugin import BasePlugin, get_supported_languages, load_config, load_module
from utils.pattern.pattern_detector import PatternDetector

PATTERN_DIRECTORY_NAME = "plugins"
PATTERN_MOD_NAME = "pattern"


class PluginPatternEntrypointBase(BasePlugin):

    def get_pattern(self):
        return self.pattern

    @abstractmethod
    def output(self, unconsolidated_lax_dict=None, consolidated_lax_dict=None, strict_ent_dict=None,
               validate_dict=None):
        result_dict = {}
        for _dict in [unconsolidated_lax_dict, consolidated_lax_dict, strict_ent_dict, validate_dict]:
            if _dict is None:
                continue
            for _key in _dict.keys():
                result_dict.update(_dict[_key])
        if result_dict == {}:
            result = {}
        else:
            result = {self._plugin_key: result_dict}
        return result

    def _load_pattern_by_lang(self, is_lang_dependent, plugin_path):
        """
            is_lang_dependent: Returns True if there are language directories.
            supported_lang: List of supported languages.
            lang: language of the text to be analyzed.
            plugin_path: plugin directory.
        """
        plugin_path = os.path.basename(plugin_path)
        lang = self.lang.lower()
        is_supported_lang = (lang in self.supported_languages)
        if is_lang_dependent and is_supported_lang:
            plugin_path = plugin_path + "." + lang
        module = PATTERN_DIRECTORY_NAME + "." + plugin_path + "." + PATTERN_MOD_NAME
        return load_module(module).PluginPattern()

    def __init__(self, plugin_path, is_lang_dependent, plugin_key, lang, text):
        super().__init__(text, lang)
        self._plugin_key = plugin_key
        self.supported_languages = get_supported_languages(plugin_path)
        self.pattern = self._load_pattern_by_lang(is_lang_dependent, plugin_path)

    @abstractmethod
    def run(self):
        detector = PatternDetector(self.text, self.lang, self.get_pattern())
        unique_strict_ent_dict, unique_consolidated_broad_dict, unique_unconsolidated_broad_dict, unique_validate_list \
            = detector.run()
        return self.output(unconsolidated_lax_dict=unique_unconsolidated_broad_dict,
                           consolidated_lax_dict=unique_consolidated_broad_dict,
                           strict_ent_dict=unique_strict_ent_dict,
                           validate_dict=unique_validate_list)
