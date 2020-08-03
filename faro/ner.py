#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from .utils import preprocess_text


logger = logging.getLogger(__name__)


class NER(object):
    """ A class to extract entities using different NERs """

    @staticmethod
    def _spacy(doc, ent_list):
        # using SpaCy
        for ent in doc.ents:
            if ent.label_.upper() in ["PER", "ORG"]:
                ent_list.append((ent.text, ent.label_.upper(), ent.start_char, ent.end_char, ent.start))

    def _spacy_extra_models(self, u_text, ent_list):
        if self.nlp_extra is not None:
            for nlp_e in self.nlp_extra:
                doc = nlp_e(u_text)

                for ent in doc.ents:
                    ent_list.append((ent.text, ent.label_, ent.start_char, ent.end_char, ent.start))


    def get_model_entities(self, sentence):
        """ Get enttities with a NER ML model (Spacy)

        Keyword arguments:
        sentence -- a string with a sentence or paragraph

        """

        u_text = preprocess_text(sentence)

        doc = self.nlp(u_text)

        # extracting entities with spacy
        ent_list = []

        # Detect entities: PER -> Persons and ORG -> Organizations
        self._spacy(doc, ent_list)

        # extracting entities with crfs
        self._spacy_extra_models(u_text, ent_list)
        return ent_list

    def __init__(self, nlp, nlp_extra=None):
        """ Initialization

        Keyword arguments:
        nlp: spacy model
        nlp_extra: additional spacy models (e.g. with custom entities) (default None)
        """

        self.nlp = nlp
        self.nlp_extra = nlp_extra
