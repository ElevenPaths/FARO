#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from utils.features.ner import NER
from utils.features.entrypoint_feature_base import PluginFeatureEntrypoint as FeatureEntrypointBase
from utils.features.feature_detector import FeatureDetector
from utils.features.spacy import Spacy

feature_path = os.path.dirname(os.path.abspath(__file__))


class PluginEntrypoint(FeatureEntrypointBase):

    def _get_instance(self):
        lang = self.get_lang()
        return NER(Spacy(), lang=lang, entity="ORG")

    def detector(self, sent):
        return self._instance.get_model_entities(sent)

    def __init__(self, text, lang):
        self.is_lang_dependent = True
        super().__init__(self.is_lang_dependent, lang, text)
        self._instance = self._get_instance()

    def run(self):
        detector = FeatureDetector(self.text, self.lang, self)
        unique_list = detector.run()
        return self.output(unique_list)

