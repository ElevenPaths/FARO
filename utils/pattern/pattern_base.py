#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.utils import clean_text


class PluginPatternBase:
    def get_strict_regexp(self):
        return self.dict_regex_strict

    def get_lax_regexp(self):
        return self.dict_regex_lax

    def get_strict_entities(self):
        return self._strict_entities

    def get_consolidated_lax_entities(self):
        return self._consolidated_entities

    def get_unconsolidated_lax_entities(self):
        return self._unconsolidated_entities

    def get_plugin_path(self):
        return self.plugin_path

    @staticmethod
    def _dict_to_regex_struct(_dict):
        if not _dict:
            return []
        return [(k, v) for v, k in _dict.items()]

    @staticmethod
    def clean_entity(text):
        return clean_text(text)

    def strict_regexp(self):
        pass

    def lax_regexp(self):
        pass

    def validate(self, ent):
        pass

    def __init__(self, plugin_path, regex_lax, regex_strict):
        self._strict_entities = {}
        self._consolidated_entities = {}
        self._unconsolidated_entities = {}

        self.dict_regex_lax = self._dict_to_regex_struct(regex_lax)
        self.dict_regex_strict = self._dict_to_regex_struct(regex_strict)
        self.plugin_path = plugin_path
