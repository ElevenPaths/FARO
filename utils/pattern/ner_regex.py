#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import copy
import re

from utils.utils import normalize_text, clean_text

logger = logging.getLogger(__name__)


class RegexNer(object):
    """ Detection of some number-based entities with regular expressions """

    def _detect_regexp(self, sentence, _type):
        """ Use broad/strict coverage regexp to detect possible entities

        Keyword arguments:
        sentence -- string containing the sentence
        _type -- type of regexp [broad or strict]

        """
        result_dict = []

        for _regexp in self.regexp_compiler_dict[_type]:
            it = _regexp[0].finditer(sentence)

            for match in it:
                result_dict.append(
                    (sentence[match.start():match.end()],
                     _regexp[1], match.start(), match.end()))

        return result_dict

    @staticmethod
    def _match_found(word_list, span_text, result_dict, _regexp):
        is_match_found = False
        for _word in word_list:
            if _word in span_text:
                is_match_found = True
                break
        if is_match_found:
            result_dict.append(_regexp)
        return is_match_found

    def _check_proximity_conditions(self, unconsolidated_dict, full_text, offset):
        """ Check the proximity of keywords to a regexp detection

        Keyword arguments:
        unconsolidated_dict -- dict with entities that were not consolidated
        result_dict -- dict to store consolidated entities
        full_text -- a full document
        offset -- offset in the full document of the current sentence

        """
        result_dict = []
        is_left_search = "Context-left" in self.regexp_config_dict
        is_right_search = "Context-right" in self.regexp_config_dict

        if is_left_search:
            left_word_list = self.regexp_config_dict["Context-left"]["word_list"]
            left_span_len = self.regexp_config_dict["Context-left"]["span_len"]
        if is_right_search:
            right_word_list = self.regexp_config_dict["Context-right"]["word_list"]
            right_span_len = self.regexp_config_dict["Context-right"]["span_len"]

        for _regexp in unconsolidated_dict:
            idx_reg_start = _regexp[2] + offset
            idx_reg_end = _regexp[3] + offset
            is_stop = False
            if is_left_search:
                span_start = idx_reg_start - left_span_len
                span_end = idx_reg_end
                # safety check: span_start cannot be lower than 0 (beginning of file)
                if span_start < 0:
                    span_start = 0
                span_text = normalize_text(full_text[span_start:span_end])
                is_stop = self._match_found(left_word_list, span_text, result_dict, _regexp)

            if is_right_search and not is_stop:
                span_start = idx_reg_start
                span_end = idx_reg_end + right_span_len
                span_text = normalize_text(full_text[span_start:span_end])
                self._match_found(right_word_list, span_text, result_dict, _regexp)
        return result_dict

    @staticmethod
    def _remove_unconsolidated_matches(consolidated_list, unconsolidated_list):
        return list(set(unconsolidated_list) - set(consolidated_list))

    def _validate_list(self, validate_list, _list):
        new_list = []
        for regexp in _list:
            ent = clean_text(regexp[0])
            # print("ent: " + ent)
            if self._func_validate(ent):
                # print("\tent:" + ent + " is valid!")
                validate_list.append(regexp)
            else:
                # print("\tent:" + ent + " NO valid!")
                new_list.append(regexp)
        return validate_list, new_list

    def _validate(self, strict_list, consolidated_list):
        validate_list = []
        if self._is_validate:
            validate_list, new_strict_list = self._validate_list(validate_list, strict_list)
            validate_list, new_broad_list = self._validate_list(validate_list, consolidated_list)
        else:
            new_strict_list = strict_list
            new_broad_list = consolidated_list
        return validate_list, new_strict_list, new_broad_list

    def regex_detection(self, sentence, full_text=None, offset=0):
        """ Detect entities with a regex in sentence

        Keyword arguments:
        sentence -- a sentence in plain text

        """
        # dict to store detections
        unconsolidated_broad_list = []

        result_broad_list = self._detect_regexp(sentence, "broad")
        strict_list = copy.deepcopy(self._detect_regexp(sentence, "strict"))

        consolidated_list = [clean_text(regexp[0]) for regexp in strict_list]

        for _broad_regexp in result_broad_list:
            if clean_text(_broad_regexp[0]) not in consolidated_list:
                unconsolidated_broad_list.append(_broad_regexp)

        # check proximity conditions of broad regexp detections
        # Si no se inicializa a [] se duplican resultados
        consolidated_broad_list = self._check_proximity_conditions(unconsolidated_broad_list, full_text, offset)

        # Validate
        validate_list, strict_list, consolidated_broad_list = self._validate(strict_list,
                                                                             consolidated_broad_list)

        unconsolidated_broad_list = self._remove_unconsolidated_matches(consolidated_broad_list,
                                                                        unconsolidated_broad_list)

        return strict_list, consolidated_broad_list, unconsolidated_broad_list, validate_list

    def __init__(self, broad_regexp_dict, strict_regexp_dict, func_validate, regexp_config_dict=None):
        """ Initialization

        The process of the application of the regexp is the following:
        First and wide coverage regexp is applied to extract as many
        candidates as possible. ["broad"

        Keyword arguments:
        broad_regexp_dict -- a dict containing the broad coverage regexp
        strict_regexp_dict -- a dict containing stricter regexp
        regexp_config_dict -- a dict containing the configuration
                              on the proximity conditions

        """

        self._is_validate = func_validate is not None
        self._func_validate = func_validate

        if regexp_config_dict is None:
            regexp_config_dict = {}

        self.regexp_compiler_dict = {"broad": []}

        for _regexp in broad_regexp_dict:
            self.regexp_compiler_dict["broad"].append((re.compile(_regexp[0]), _regexp[1]))

        self.regexp_compiler_dict["strict"] = []

        for _regexp in strict_regexp_dict:
            self.regexp_compiler_dict["strict"].append((re.compile(_regexp[0]), _regexp[1]))

        self.regexp_config_dict = regexp_config_dict
