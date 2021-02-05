#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.base_detector import BaseDetector, get_unique_ents


class FeatureDetector(BaseDetector):
    """ Main class for extracting KPIs of confidential documents
    """

    def get_kpis(self, sent_list):
        """ Extract KPIs from document """
        # full_text is used for proximity detection
        full_text = "".join(sent_list)
        total_ent_list = []

        offset = 0

        for sent in sent_list:
            line_length = len(sent)

            result = self.custom_detector.detector(sent)
            total_ent_list.extend(result)

            offset += line_length

        return total_ent_list

    def run(self):
        """ Obtain KPIs from a document and obtain the output in the right format (json)

        Keyword arguments:
        content -- list of sentences to obtain the entities

        """
        ent_list = self.get_kpis(self.text)
        unique_list = get_unique_ents(ent_list)
        return unique_list

    def __init__(self, text, lang, custom_detector):
        """ Intialization

        Keyword Arguments:
        config -- a dict with yaml configuration parameters

        Properties
        nlp -- a spacy model or None
        custom_word_list -- list with custom words
        regexp_config_dict -- configuration of the proximity detections
        signature_max_distance -- maximum distance between distance and signature
        low_priority_list -- list of entity types with low priority

        """
        super().__init__(text, lang)
        self.text = text
        self.custom_detector = custom_detector
