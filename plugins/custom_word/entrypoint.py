#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from utils.features.entrypoint_feature_base import PluginFeatureEntrypoint as FeatureEntrypointBase
from utils.features.feature_detector import FeatureDetector
from .custom_word import CustomWordDetector

feature_path = os.path.dirname(os.path.abspath(__file__))
_KEY = "CUSTOM"


class PluginEntrypoint(FeatureEntrypointBase):

    def _get_instance(self):
        lang_path = self.get_path_lang(feature_path)
        lang = self.get_lang()
        return CustomWordDetector(lang, lang_path)

    def detector(self, sent):
        return self._instance.search_custom_words(sent)

    def __init__(self, text, lang):
        self.is_lang_dependent = True
        super().__init__(self.is_lang_dependent, lang, text)
        self._instance = self._get_instance()

    def run(self):
        detector = FeatureDetector(self.text, self.lang, self)
        unique_list = detector.run()
        return self.output(unique_list)

