#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import spacy
from .utils import normalize_text, clean_text
from stdnum import get_cc_module
from stdnum.luhn import validate
from stdnum.exceptions import InvalidChecksum, InvalidFormat
from .ner import NER
from .email import EmailFilter
from .ner_regex import RegexNer
from .custom_word import CustomWordDetector
from collections import OrderedDict

CWD = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(CWD, '..', 'config')
MODELS_PATH = os.path.join(CWD, '..', 'models')
_COMMONS_YAML = "%s/commons.yaml" % CONFIG_PATH

logger = logging.getLogger(__name__)


class Detector(object):
    """ Main class for extracting KPIs of confidential documents

    """

    def _get_signature(self, person_signed_idx, next_person_has_signed, total_ent_list):
        if next_person_has_signed:
            min_itx_signed = self.signature_max_distance
            id_min_itx = -1

            for i in range(len(total_ent_list)):
                ent = total_ent_list[i]
                if ent[1] == "PER" and int(ent[3]) > person_signed_idx and int(
                        ent[3]) - person_signed_idx < min_itx_signed:
                    min_itx_signed = int(ent[3]) - person_signed_idx
                    id_min_itx = i
                    next_person_has_signed = False

            if id_min_itx != -1:
                ent = total_ent_list[id_min_itx]
                total_ent_list.append((ent[0], "SIGNATURE", ent[2], ent[3], ent[4]))

    def _extract_entities_ml(self, sent, offset, total_ent_list):
        if self.ml_ner is not None:
            ent_list_ner = self.ml_ner.get_model_entities(sent)

            for ent in ent_list_ner:
                # storing as entity/label pair
                new_ent = [ent[0],
                           ent[1],
                           "NER",
                           str(int(ent[2]) + offset),
                           str(int(ent[3]) + offset)]

                total_ent_list.append(new_ent)

    def _entity_regex_email(self, ent, offset, total_ent_list):
        if self.corp_email_class.is_corp_email(ent[0]):
            total_ent_list.append((
                ent[0],
                "CORP_EMAIL",
                ent[1],
                str(ent[2] + offset),
                str(ent[3] + offset)))
        else:
            total_ent_list.append((ent[0],
                                   "EMAIL",
                                   ent[1],
                                   str(ent[2] + offset),
                                   str(ent[3] + offset)))

    @staticmethod
    def _entity_regex_credit_card(ent, offset, total_ent_list):
        sent = clean_text(ent[0])
        try:
            if validate(sent):
                logger.debug(
                    "Credit card accepted {}.{}".format(sent, ent[0]))

                total_ent_list.append((ent[0],
                                       "FINANCIAL_DATA",
                                       ent[1],
                                       str(ent[2] + offset),
                                       str(ent[3] + offset)))

        except (InvalidChecksum, InvalidFormat):
            logger.debug("Wrong credit card {}.{}.".format(sent, ent[0]))

    def _entity_signed_person(self, total_ent_list, person_signed_idx, next_person_has_signed):
        min_itx_signed = self.signature_max_distance
        id_min_itx = -1

        for i in range(len(total_ent_list)):
            _ent = total_ent_list[i]

            if _ent[1] == "PER" and int(_ent[3]) > person_signed_idx and int(
                    _ent[3]) - person_signed_idx < min_itx_signed:
                min_itx_signed = (int(_ent[3]) - person_signed_idx)
                id_min_itx = i
                next_person_has_signed = False

        if id_min_itx != -1:
            _ent = total_ent_list[id_min_itx]

            total_ent_list.append((_ent[0], "SIGNATURE", _ent[2], _ent[3], _ent[4]))
        return next_person_has_signed

    @staticmethod
    def _entity_financial_data(ent, ent_key, offset, total_ent_list):
        sent = clean_text(ent[0])
        if get_cc_module('es', 'ccc').is_valid(sent) or get_cc_module('es', 'iban').is_valid(sent):
            total_ent_list.append((ent[0], ent_key, ent[1], str(ent[2] + offset), str(ent[3] + offset)))
        else:
            logger.debug("Invalid financial data {}.{}".format(sent, ent[0]))

    @staticmethod
    def _entity_id_document(ent, ent_key, offset, total_ent_list):
        sent = clean_text(ent[0])
        if (get_cc_module('es', 'dni').is_valid(sent) or
                get_cc_module('es', 'cif').is_valid(sent) or
                get_cc_module('es', 'nie').is_valid(sent)):
            total_ent_list.append((ent[0], ent_key, ent[1], str(ent[2] + offset), str(ent[3] + offset)))
        else:
            logger.debug("Invalid data ID document {}.{}".format(sent, ent[0]))

    def _extract_entities_regex(self, offset, sent, full_text, total_ent_list, next_person_has_signed):
        ent_list_regex = self.regex_ner.regex_detection(sent, full_text, offset)

        for ent_key in ent_list_regex.keys():
            for ent in ent_list_regex[ent_key]:

                # We treat differently common corporative/personal emails
                if ent_key == "EMAIL":
                    self._entity_regex_email(ent, offset, total_ent_list)

                elif ent_key == "SIGNATURE":
                    next_person_has_signed = True
                    person_signed_idx = int(ent[3]) + offset

                elif ent_key == "CREDIT_CARD":
                    self._entity_regex_credit_card(ent, offset, total_ent_list)
                elif ent_key == "FINANCIAL_DATA":
                    self._entity_financial_data(ent, ent_key, offset, total_ent_list)
                elif ent_key == "ID_DOCUMENT":
                    self._entity_id_document(ent, ent_key, offset, total_ent_list)
                else:
                    total_ent_list.append((ent[0],
                                           ent_key,
                                           ent[1],
                                           str(ent[2] + offset),
                                           str(ent[3] + offset)))
        if next_person_has_signed:
            self._entity_signed_person(total_ent_list, person_signed_idx, next_person_has_signed)

    def _detection_custom_word(self, sent, offset, total_ent_list):
        custom_list = self.custom_detector.search_custom_words(sent)
        for _ent in custom_list:
            total_ent_list.append((_ent[0],
                                   _ent[1],
                                   _ent[0],
                                   str(_ent[2] + offset),
                                   str(_ent[3] + offset)))

    def _get_kpis(self, sent_list):
        """ Extract KPIs from document """

        # full_text is used for proximity detection
        full_text = "".join(sent_list)

        total_ent_list = []

        # Flag to indicate that a sign entity is expected (if True)
        next_person_has_signed = False
        person_signed_idx = 0

        offset = 0

        for sent in sent_list:
            line_length = len(sent)

            # extract entities (ML)
            self._extract_entities_ml(sent, offset, total_ent_list)

            # extract entities (Regex)
            self._extract_entities_regex(offset, sent, full_text, total_ent_list, next_person_has_signed)

            # detection of custom words
            self._detection_custom_word(sent, offset, total_ent_list)

            offset += line_length

        self._get_signature(person_signed_idx, next_person_has_signed, total_ent_list)

        return total_ent_list

    @staticmethod
    def _get_unique_ents(ent_list):
        """ Process the entities to obtain a json object """
        unique_ent_dict = {}
        for _ent in ent_list:
            if _ent[1] not in unique_ent_dict:
                unique_ent_dict[_ent[1]] = {}
            if _ent[0] not in unique_ent_dict[_ent[1]]:
                unique_ent_dict[_ent[1]][_ent[0]] = 0
            unique_ent_dict[_ent[1]][_ent[0]] += 1
        return unique_ent_dict

    def analyse(self, content):
        """ Obtain KPIs from a document and obtain the output in the right format (json)

        Keyword arguments:
        content -- list of sentences to obtain the entities

        """
        total_ent_list = self._get_kpis(content)
        unique_ent_dict = self._get_unique_ents(total_ent_list)
        return unique_ent_dict

    def __init__(self, config):
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

        # build the system here
        nlp = None
        cfg_section = "ner_config"
        cfg_item = "nlp_model"
        if cfg_section in config and cfg_item in config[cfg_section]:
            nlp = spacy.load(config[cfg_section][cfg_item])

        # Custom word that the organization wants to detect as sensitive
        custom_word_list = []
        cfg_section = "custom_config"
        cfg_item = "word_file"
        if cfg_section in config and cfg_item in config[cfg_section]:
            with open('%s/%s' % (CONFIG_PATH, config[cfg_section][cfg_item]), "r") as f_in:
                custom_word_list = [line.rstrip("\n") for line in f_in]

        # configuration of the proximity regexp
        regexp_config_dict = {}
        if "regexp_config" in config:
            for key in config["regexp_config"]:
                regexp_config_dict[key] = {}
                regexp_config_dict[key]["left_span_len"] = int(config["regexp_config"][key]["left_span_len"])
                regexp_config_dict[key]["right_span_len"] = int(config["regexp_config"][key]["right_span_len"])

                with open('%s/%s' % (
                        CONFIG_PATH, config["regexp_config"][key]["word_file"]), "r") as f_in:
                    word_list = [normalize_text(line.rstrip("\n").strip()) for line in f_in]

                regexp_config_dict[key]["word_list"] = word_list

        # Email filter known corporative (non sensitive) email accounts
        cfg_section = "email_config"
        cfg_item = "excl_file"
        if cfg_section in config and cfg_item in config[cfg_section]:
            with open('%s/%s' % (CONFIG_PATH, config[cfg_section][cfg_item]), "r") as f_in:
                excl_corp_list = [line.rstrip("\n") for line in f_in]

        if nlp is not None:
            self.ml_ner = NER(nlp, None)
        else:
            self.ml_ner = None

        self.custom_detector = CustomWordDetector(nlp, custom_word_list)

        self.regex_ner = RegexNer(regexp_config_dict=regexp_config_dict)
        self.corp_email_class = EmailFilter(excl_corp_list)

        max_distance = config["features"]["SIGNATURE"]["max_distance"]
        self.signature_max_distance = max_distance
