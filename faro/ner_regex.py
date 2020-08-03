#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import copy
import re
from .utils import clean_text, normalize_text

logger = logging.getLogger(__name__)

# Email
STRICT_REG_EMAIL_ADDRESS_V0 = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

# Credit Card
STRICT_REG_CREDIT_CARD_V0 = (
    r"(?:(?P<visa>((?<![0-9])(?<![0-9][,.]))4[0-9]{12}(?:[0-9]{3})?)|(?P<mastercard>((?<![0-9])(?<![0-9][,.]))5[1-5][0-9]{14})|(?P<discover>((?<![0-9])(?<![0-9][,.]))6(?:011|5[0-9][0-9])[0-9]{12}))")
BROAD_REG_CREDIT_CARD_GEN_V1 = r"([0-9][\s\-_\.]*){8,}"

# Financial Data
STRICT_REG_IBAN_V1 = r"\b[a-zA-Z]{2}[\s\-_]*[0-9]{2}([\s\-_]*[0-9]{4}){5}\b"
BROAD_REG_IBAN_APPROX_V1 = r"[a-zA-Z]{2}[\s\-_]*[0-9]{2}([\s\-_]*[0-9]{4}){5}"

# DNI_SPAIN
STRICT_REG_DNI_V0 = r"(\b|[\(]|\bnº|\bNº)[0-9,X,M,L,K,Y][\-\. ]?[0-9]{7}[\-\. ]?[A-Z](\b|[\)\.\],:])"
STRICT_REG_CIF_V0 = r"(\b|[\(]|\bnº|\bNº)[A-Za-z][\-\.\s]?[0-9]{2}(\.?)[0-9]{3}(\.?)[0-9]{3}(\b|[\)\.\],:])"
BROAD_REG_DNI_GEN_V0 = r"[0-9,X,M,L,K,Y][\-\. ]?[0-9]{7}[\-\. ]?[A-Z]?"
BROAD_REG_CIF_GEN_V0 = r"[A-Za-z][\-\.\s]?[0-9]{2}([\.\-\s]?)[0-9]{3}([\-\.\s]?)[0-9]{3}"

# Money
STRICT_REG_EURO_V0 = r"(?i)\b(\d+\.)*\d+(,\d{2,})*(\.\d*)?(?=(\s*€|\s*euros\b|\s*de\s+euros\b|\s*eur\b))"

# Prob Currency
STRICT_REG_MONEY_V0 = r"\b(?<!\.)\d+(\.\d{3,})+(,\d{2,})*(\.\d*)?\b"
STRICT_REG_MONEY_V1 = r"\b(?<![,\.])\d+(,\d{2,})\b"

# Phone
BROAD_REG_PHONE_NUMBER_GEN_V3 = r"(\(?\s*(\+34|0034|34)\s*\)?\s*)?[89](\s+|-\.)?([0-9](\s+|-|\.)?){8}"

# r"(\(?\s*(\+34|0034|34)\s*\)?\s*)?(?<![0-9])[\s|\-|\.]?[8|9][\s+|\-|\.]?([0-9][\s+|\-|\.]?){8}(\s+|\b)(?!(?:\s?[0-9]){1,})"

# Mobile
BROAD_REG_MOBILE_NUMBER_GEN_V3 = r"[67](\s+|-\.)?([0-9](\s+|-|\.)?){8}"

# Signature
STRICT_REG_FIRMA_V0 = r"Firmado por|Firmado|Fdo\.|Signed by|Firma\s|firma del representante"

DICT_REGEX_STRICT = {"EMAIL": [(STRICT_REG_EMAIL_ADDRESS_V0,
                                "STRICT_REG_EMAIL_ADDRESS_V0")],
                     "CREDIT_CARD": [(STRICT_REG_CREDIT_CARD_V0,
                                      "STRICT_REG_CREDIT_CARD_V0")],
                     "FINANCIAL_DATA": [(STRICT_REG_IBAN_V1,
                                         "STRICT_REG_IBAN_V1")],
                     "ID_DOCUMENT": [(STRICT_REG_DNI_V0, "STRICT_REG_DNI_V0"),
                                     (STRICT_REG_CIF_V0, "STRICT_REG_CIF_V0"),
                                     ],
                     "MONEY": [(STRICT_REG_EURO_V0,
                                "STRICT_REG_EURO_V0")],
                     "PROB_CURRENCY": [(STRICT_REG_MONEY_V0,
                                        "STRICT_REG_MONEY_V0"),
                                       (STRICT_REG_MONEY_V1,
                                        "STRICT_REG_MONEY_V1")],
                     "SIGNATURE": [(STRICT_REG_FIRMA_V0,
                                    "STRICT_REG_FIRMA_V0")]}

DICT_REGEX_BROAD = {"CREDIT_CARD": [(BROAD_REG_CREDIT_CARD_GEN_V1,
                                     "BROAD_REG_CREDIT_CARD_GEN_V1")],
                    "FINANCIAL_DATA": [(BROAD_REG_IBAN_APPROX_V1,
                                        "BROAD_REG_IBAN_APPROX_V1")],
                    "ID_DOCUMENT": [(BROAD_REG_DNI_GEN_V0,
                                     "BROAD_REG_DNI_GEN_V0"),
                                    (BROAD_REG_CIF_GEN_V0,
                                     "BROAD_REG_CIF_GEN_V0"),
                                    ],
                    "PHONE": [
                        (BROAD_REG_PHONE_NUMBER_GEN_V3,
                         "BROAD_REG_PHONE_NUMBER_GEN_V3"),
                    ],
                    "MOBILE": [
                        (BROAD_REG_MOBILE_NUMBER_GEN_V3,
                         "BROAD_REG_MOBILE_NUMBER_GEN_V3")]}


class RegexNer(object):
    """ Detection of some number-based entities with regular expressions """

    def _detect_regexp(self, sentence, _type):
        """ Use broad/strict coverage regexp to detect possible entities

        Keyword arguments:
        sentence -- string containing the sentence
        _type -- type of regexp [broad or strict]

        """

        result_dict = {}

        for _regexp_key in self.regexp_compiler_dict[_type]:
            for _regexp in self.regexp_compiler_dict[_type][_regexp_key]:
                it = _regexp[0].finditer(sentence)

                for match in it:
                    if _regexp_key not in result_dict:
                        result_dict[_regexp_key] = []

                    result_dict[_regexp_key].append(
                        (sentence[match.start():match.end()],
                         _regexp[1], match.start(), match.end()))

        return result_dict

    @staticmethod
    def _match_found(word_list, span_text, key, result_dict, _regexp):
        match_found = False
        for _word in word_list:
            if _word in span_text:
                match_found = True
                break
        if match_found:
            if key not in result_dict:
                result_dict[key] = []
            result_dict[key].append(_regexp)

    def _check_proximity_conditions(self, unconsolidated_dict,
                                    result_dict,
                                    full_text,
                                    offset):
        """ Check the proximity of keywords to a regexp detection

        Keyword arguments:
        unconsolidated_dict -- dict with entities that were not consolidated
        result_dict -- dict to store consolidated entities
        full_text -- a full document
        offset -- offset in the full document of the current sentence

        """

        for key in unconsolidated_dict:
            if key in self.regexp_config_dict:
                left_span_len = self.regexp_config_dict[key]["left_span_len"]
                right_span_len = self.regexp_config_dict[key]["right_span_len"]
                word_list = self.regexp_config_dict[key]["word_list"]

                for _regexp in unconsolidated_dict[key]:
                    idx_reg_start = _regexp[2] + offset
                    idx_reg_end = _regexp[3] + offset

                    span_start = idx_reg_start - left_span_len
                    span_end = idx_reg_end + right_span_len

                    # safety check: span_start cannot be lower than 0 (beginning of file)
                    if span_start < 0:
                        span_start = 0

                    span_text = normalize_text(
                        full_text[span_start:span_end])

                    self._match_found(word_list, span_text, key, result_dict, _regexp)

    def regex_detection(self, sentence, full_text=None, offset=0):
        """ Detect entities with a regex in sentence

        Keyword arguments:
        sentence -- a sentence in plain text

        """

        # dict to store the consolidated detections
        unconsolidated_dict = {}

        result_broad_dict = self._detect_regexp(sentence, "broad")
        # entities that pass the strict regexp are automatically validated
        result_dict = copy.deepcopy(self._detect_regexp(sentence, "strict"))

        for key in result_broad_dict:
            consolidated_list = []

            if key in result_dict:
                # get the consolidated regexp
                consolidated_list = [clean_text(regexp[0]) for regexp in result_dict[key]]

            for _broad_regexp in result_broad_dict[key]:
                if clean_text(_broad_regexp[0]) not in consolidated_list:
                    if key not in unconsolidated_dict:
                        unconsolidated_dict[key] = []

                    unconsolidated_dict[key].append(_broad_regexp)

        # check proximity conditions of broad regexp detections
        self._check_proximity_conditions(unconsolidated_dict,
                                         result_dict,
                                         full_text,
                                         offset)

        return result_dict

    def __init__(self, broad_regexp_dict=DICT_REGEX_BROAD,
                 strict_regexp_dict=DICT_REGEX_STRICT,
                 regexp_config_dict=None):
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

        if regexp_config_dict is None:
            regexp_config_dict = {}

        self.regexp_compiler_dict = {"broad": {}}

        for _regexp_key in broad_regexp_dict:
            self.regexp_compiler_dict["broad"][_regexp_key] = []

            for _regexp in broad_regexp_dict[_regexp_key]:
                self.regexp_compiler_dict["broad"][_regexp_key].append(
                    (re.compile(_regexp[0]), _regexp[1]))

        self.regexp_compiler_dict["strict"] = {}
        for _regexp_key in strict_regexp_dict:
            self.regexp_compiler_dict["strict"][_regexp_key] = []

            for _regexp in strict_regexp_dict[_regexp_key]:
                self.regexp_compiler_dict["strict"][_regexp_key].append(
                    (re.compile(_regexp[0]), _regexp[1]))

        self.regexp_config_dict = regexp_config_dict
