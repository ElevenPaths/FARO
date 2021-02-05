#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from pathlib import Path

import yaml

from utils.base_detector import BaseDetector, get_unique_ents, CWD
from utils.pattern.ner_regex import RegexNer
from utils.utils import normalize_text

CONFIG_PATH = os.path.join(CWD, '..', 'config')
MODELS_PATH = os.path.join(CWD, '..', 'models')
_COMMONS_YAML = "%s/commons.yaml" % CONFIG_PATH

_REGEXP_CONFIG_KEY_NAME = "regexp_config"
_CONTEXT_KEY_NAME = "Context"
_CONTEXT_LEFT_KEY_NAME = "Context-left"
_CONTEXT_RIGHT_KEY_NAME = "Context-right"
_SPAN_LEN_PARAM_NAME = "span_len"
_WORD_FILE_PARAM_NAME = "word_file"
_WORD_LIST_NAME = "word_list"


class PatternDetector(BaseDetector):
    """ Main class for extracting KPIs of confidential documents
    """

    def _load_context(self, plugin_path):
        context_yaml = "%s/context.yaml" % plugin_path
        regexp_config_dict = {}
        if Path(context_yaml).is_file():
            with open(context_yaml, "r", encoding='utf8') as f_stream:
                context = yaml.load(f_stream, Loader=yaml.FullLoader)

                # configuration of the proximity regexp
                regexp_config_dict = {}
                if _REGEXP_CONFIG_KEY_NAME in context:

                    if _CONTEXT_KEY_NAME in context[_REGEXP_CONFIG_KEY_NAME]:
                        context_word = self._load_word_file(plugin_path, context[_REGEXP_CONFIG_KEY_NAME][_CONTEXT_KEY_NAME][_WORD_FILE_PARAM_NAME])

                    if _CONTEXT_LEFT_KEY_NAME in context[_REGEXP_CONFIG_KEY_NAME]:
                        regexp_config_dict[_CONTEXT_LEFT_KEY_NAME] = {}
                        regexp_config_dict[_CONTEXT_LEFT_KEY_NAME][_SPAN_LEN_PARAM_NAME] = int(
                            context[_REGEXP_CONFIG_KEY_NAME][_CONTEXT_LEFT_KEY_NAME][_SPAN_LEN_PARAM_NAME])
                        context_left_word = self._load_word_file(plugin_path, context[_REGEXP_CONFIG_KEY_NAME][_CONTEXT_LEFT_KEY_NAME][_WORD_FILE_PARAM_NAME])
                        context_left_word.extend(context_word)
                        regexp_config_dict[_CONTEXT_LEFT_KEY_NAME][_WORD_LIST_NAME] = context_left_word

                    if _CONTEXT_RIGHT_KEY_NAME in context[_REGEXP_CONFIG_KEY_NAME]:
                        regexp_config_dict[_CONTEXT_RIGHT_KEY_NAME] = {}
                        regexp_config_dict[_CONTEXT_RIGHT_KEY_NAME][_SPAN_LEN_PARAM_NAME] = int(
                            context[_REGEXP_CONFIG_KEY_NAME][_CONTEXT_LEFT_KEY_NAME][_SPAN_LEN_PARAM_NAME])
                        context_right_word = self._load_word_file(plugin_path, context[_REGEXP_CONFIG_KEY_NAME][_CONTEXT_RIGHT_KEY_NAME][_WORD_FILE_PARAM_NAME])
                        context_right_word.extend(context_word)
                        regexp_config_dict[_CONTEXT_RIGHT_KEY_NAME][_WORD_LIST_NAME] = context_right_word

        return regexp_config_dict

    def get_kpis(self, sent_list):
        """ Extract KPIs from document """
        # full_text is used for proximity detection
        full_text = "".join(sent_list)
        total_ent_strict_list = []
        ent_consolidated_list = []
        ent_unconsolidated_list = []
        ent_validate_list = []
        valid_regex = []

        offset = 0

        for sent in sent_list:
            line_length = len(sent)

            # extract entities (ML)
            # self._extract_entities_ml(sent, offset, total_ent_strict_list)
            strict_regex, con_broad_regex, uncon_broad_regex, valid_regex = self.regex_ner.regex_detection(sent,
                                                                                                           full_text,
                                                                                                           offset)
            total_ent_strict_list.extend(strict_regex)
            ent_consolidated_list.extend(con_broad_regex)
            ent_unconsolidated_list.extend(uncon_broad_regex)
            ent_validate_list.extend(valid_regex)

            offset += line_length

        return total_ent_strict_list, ent_consolidated_list, ent_unconsolidated_list, ent_validate_list

    def run(self):
        """ Obtain KPIs from a document and obtain the output in the right format (json)

        """

        total_ent_strict_list, consolidated_broad_list, unconsolidated_broad_list, validate_list = self.get_kpis(
            self.text)
        unique_strict_ent_dict = get_unique_ents(total_ent_strict_list)
        unique_consolidated_broad_dict = get_unique_ents(consolidated_broad_list)
        unique_unconsolidated_broad_dict = get_unique_ents(unconsolidated_broad_list)
        unique_validate_list = get_unique_ents(validate_list)

        return unique_strict_ent_dict, unique_consolidated_broad_dict, unique_unconsolidated_broad_dict, unique_validate_list

    @staticmethod
    def _load_word_file(plugin_path, word_file_name):
        file_path = '%s/%s' % (plugin_path, word_file_name)
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding='utf8') as f_in:
                word_list = [normalize_text(line.rstrip("\n").strip()) for line in f_in if line != "\n"]
        else:
            word_list = []
        return word_list

    def __init__(self, text, lang, pattern):
        super().__init__(text, lang)

        regexp_config_dict = self._load_context(pattern.get_plugin_path())

        dict_regex_lax = pattern.get_lax_regexp()
        dict_regex_strict = pattern.get_strict_regexp()

        # only functions without 'return' or 'pass' return None
        validation_func = pattern.validate
        if pattern.validate("") is None:
            validation_func = None

        self.regex_ner = RegexNer(dict_regex_lax, dict_regex_strict, validation_func,
                                  regexp_config_dict=regexp_config_dict)
