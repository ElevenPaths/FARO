#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from utils.utils import preprocess_text

logger = logging.getLogger(__name__)


class NER:
    """ A class to extract entities using different NERs """

    def _spacy(self, doc):
        # using SpaCy
        ent_list = []
        for ent in doc:
            if ent[1].upper() in [self.entity]:
                ent_list.append(ent)
        return ent_list

    def _spacy_extra_models(self, u_text, ent_list):
        ent_list = self.spacy.run_extra(u_text)

    def get_model_entities(self, sentence):
        """ Get entities with a NER ML model (Spacy)

        Keyword arguments:
        sentence -- a string with a sentence or paragraph

        """

        u_text = preprocess_text(sentence)

        doc, token_list = self.spacy.run(self.lang, u_text)

        ent_list = self._spacy(doc)

        # extracting entities with crfs
        # self._spacy_extra_models(u_text, ent_list)
        return ent_list

    def __init__(self, spacy, lang, entity="PER"):
        """ Initialization

        Keyword arguments:
        nlp: spacy model
        nlp_extra: additional spacy models (e.g. with custom entities) (default None)
        """

        self.spacy = spacy
        self.entity = entity
        self.lang = lang
