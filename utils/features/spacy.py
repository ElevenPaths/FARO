#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import spacy

from utils.singleton import Singleton

logger = logging.getLogger(__name__)

_SPACY_MODEL_NAME = "_core_news_"
_SPACY_DEFAULT_MODEL_NAME = "xx_ent_wiki_sm"
# lg, md, sm
_SPACY_MODEL_TYPE = "sm"


def _load_spacy_model(lang):
    model_name = '%s%s%s' % (lang, _SPACY_MODEL_NAME, _SPACY_MODEL_TYPE)
    try:
        nlp = spacy.load(model_name)
    except Exception:
        nlp = spacy.load(_SPACY_DEFAULT_MODEL_NAME)
    return nlp


class Spacy(metaclass=Singleton):
    """ A class to manage spacy models to be used as a util resource """

    def __init__(self):
        self._nlp = None
        self._nlp_extra = None
        self.max_length = 1000000
        self.ent_list = []
        self.token_list = []
        self.ent_list_extra = []
        self.processed = False
        self.last_text = ""
        self.last_lang = ""

    def run(self, lang, text):
        if self.last_lang != lang:
            self._nlp = _load_spacy_model(lang)
            self.last_lang = lang
            self.processed = False
        if self.last_text != text:
            self.last_text = text
            self.processed = False
        if not self.processed:
            self.processed = True
            self.ent_list = []
            self.token_list = []
            chunks = [text[i:i + self.max_length] for i in range(0, len(text), self.max_length)]
            for chunk in chunks:
                doc = self._nlp(chunk)
                [self.ent_list.append((ent.text, ent.label_.upper(), ent.start_char, ent.end_char, ent.start))
                 for ent in doc.ents]
                [self.token_list.append(token) for token in doc]
        return self.ent_list, self.token_list

    def run_extra(self, text):
        if self._nlp_extra is None:
            return None
        else:
            for nlp_e in self._nlp_extra:
                doc = nlp_e(text)
                for ent in doc.ents:
                    self.ent_list_extra.append((ent.text, ent.label_, ent.start_char, ent.end_char, ent.start))
            return self.ent_list_extra
