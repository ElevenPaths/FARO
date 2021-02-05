#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from abc import abstractmethod

from utils.base_plugin import BasePlugin, get_supported_languages

PATTERN_DIRECTORY_NAME = "features"


class PluginFeatureEntrypoint(BasePlugin):

    def get_lang(self):
        return self._lang

    def get_path_lang(self, path):
        _path_lang = path
        if self._is_lang_dependent:
            if self._lang in get_supported_languages(path):
                _path_lang = os.path.join(path, self._lang)
        return _path_lang

    def detection(self):
        pass

    @staticmethod
    def output(_list):
        return _list

    def __init__(self, is_lang_dependent, lang, text):
        super().__init__(text, lang)
        self._is_lang_dependent = is_lang_dependent
        self._lang = lang

    @abstractmethod
    def run(self):
        pass
