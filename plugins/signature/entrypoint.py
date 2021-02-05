#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from utils.base_detector import get_unique_ents
from utils.base_plugin import load_config
from utils.features.feature_detector import FeatureDetector
from utils.features.ner import NER
from utils.features.spacy import Spacy
from utils.pattern.entrypoint_pattern_base import PluginPatternEntrypointBase
from utils.pattern.pattern_detector import PatternDetector

_CWD = os.path.dirname(__file__)

MANIFEST = {
    "name": "Signature",
    "key": "SIGNATURE",
    "version": "0.1",
    "type": "SIGNATURE",
    "description": "Signature",
    "author": "Hugo",
    "email": "",
}


class PluginEntrypoint(PluginPatternEntrypointBase):

    def __init__(self, text, lang):
        self.is_lang_dependent = False
        super().__init__(_CWD, self.is_lang_dependent, MANIFEST["key"], lang, text)
        self.config = load_config(_CWD, "config.yaml")
        self.signature_max_distance = self.config["max_distance"]
        self.feature_ent_list = list()
        self.signatures = list()

    def detector(self, sent):
        return NER(Spacy(), self.lang).get_model_entities(sent)

    def _entity_signed_person(self, person_signed_idx):
        min_itx_signed = self.signature_max_distance
        id_min_itx = -1

        for i in range(len(self.feature_ent_list)):
            _ent = self.feature_ent_list[i]
            if _ent[1] == "PER" and int(_ent[2]) > person_signed_idx and int(
                    _ent[2]) - person_signed_idx < min_itx_signed:
                min_itx_signed = (int(_ent[2]) - person_signed_idx)
                id_min_itx = i

        if id_min_itx != -1:
            _ent = self.feature_ent_list[id_min_itx]
            self.signatures.append((_ent[0], MANIFEST["key"], _ent[2], _ent[3]))

    def update_signatures(self, total_ent_strict_list):
        for signature in total_ent_strict_list:
            self._entity_signed_person(signature[3])

    def run_feature_detector(self):
        feature_detector = FeatureDetector(self.text, self.lang, self)
        self.feature_ent_list = feature_detector.get_kpis(self.text)

    def run_pattern_detector(self):
        pattern_detector = PatternDetector(self.text, self.lang, self.get_pattern())
        total_ent_strict_list, [], [], [] = pattern_detector.get_kpis(
            self.text)
        self.update_signatures(total_ent_strict_list)
        return get_unique_ents(self.signatures)

    def output(self, unconsolidated_lax_dict=None, consolidated_lax_dict=None, strict_ent_dict=None,
               validate_dict=None):
        return super().output(strict_ent_dict=strict_ent_dict)

    def run(self):
        self.run_feature_detector()
        unique_strict_ent_dict = self.run_pattern_detector()
        return self.output(strict_ent_dict=unique_strict_ent_dict)
