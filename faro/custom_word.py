#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)


class CustomWordDetector(object):
    """ Detect custom words in texts """

    def _search_words_with_spacy(self, sentence, normalize_word=True):

        detection_list = []

        doc = self.nlp(sentence)

        for token in doc:
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

        if self.nlp:
            return self._search_words_with_spacy(sentence)
        else:
            return self._search_words_without_spacy(sentence)

    def __init__(self, nlp, word_list):
        """ Initialization """

        self.nlp = nlp
        self.word_list = [word.lower().strip() for word in word_list]
