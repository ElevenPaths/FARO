#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

from utils.features.spacy import Spacy

logger = logging.getLogger(__name__)

_CUSTOM_WORDS_FILE_NAME = "custom_words.txt"


class CustomWordDetector(object):
    """ Detect custom words in texts """

    def _search_words_with_spacy(self, sentence, normalize_word=True):

        detection_list = []

        ent_list, token_list = self.spacy.run(self.lang, sentence)

        for token in token_list:
            if (token.text.lower() in self.word_list or
                    token.lemma_.lower() in self.word_list):

                if not normalize_word:
                    detection_list.append([token.text, "CUSTOM", token.idx,
                                           token.idx + len(token.text)])
                else:
                    detection_list.append([token.lemma_.lower(),
                                           "CUSTOM", token.idx,
                                           token.idx + len(token.text)])

        return detection_list

    def _search_words_without_spacy(self, sentence):

        detection_list = []

        # simply tokenizing with spaces (FIXME use nltk instead?)

        token_offset = 0

        for token in sentence.split(" "):
            if token.lower() in self.word_list:
                detection_list.append(
                    [token, "CUSTOM", token_offset, token_offset + len(token)])

            # Update offset_t = offset_t-1 + whitespace
            token_offset += len(token) + 1

        return detection_list

    def search_custom_words(self, sentence):
        """ Search for custom words in a sentence """

        if self.spacy:
            return self._search_words_with_spacy(sentence)
        else:
            return self._search_words_without_spacy(sentence)

    @staticmethod
    def _load_word_list(path):
        word_list_path = os.path.join(path, _CUSTOM_WORDS_FILE_NAME)
        with open(word_list_path, "r", encoding='utf8') as f_in:
            return [line.rstrip("\n") for line in f_in]

    def __init__(self, lang, path):
        """ Initialization """

        # https://spacy.io/models/xx
        # xx_ent_wiki_sm
        # Supports identification of PER, LOC, ORG and MISC entities for Dutch, English, French, German, French,
        # Italian, Polish, Portuguese, Russian and Spanish.
        # Langs: Chinese, Danish, Dutch, English, French, German, Greek, Italian, Japanese, Lithuanian, Norwegian Bokmål
        # Polish, Portuguese, Romanian, Spanish

        word_list = self._load_word_list(path)
        self.spacy = Spacy()
        self.lang = lang
        self.word_list = [word.lower().strip() for word in word_list]
