#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from utils.base_detector import get_unique_ents
from utils.email import EmailFilter
from utils.pattern.entrypoint_pattern_base import PluginPatternEntrypointBase
from utils.pattern.pattern_detector import PatternDetector

_CWD = Path(__file__).parent
CONFIG_PATH = _CWD / "excl_corp_email_es.txt"

MANIFEST = {
    "name": "Email",
    "key": "EMAIL",
    "version": "0.1",
    "type": "Email",
    "description": "Email",
    "author": "Hugo",
    "email": "",
}


def config_email():
    # Email filter known corporative (non sensitive) email accounts
    with open('%s' % CONFIG_PATH, "r", encoding='utf8') as f_in:
        excl_corp_list = [line.rstrip("\n") for line in f_in]
        return excl_corp_list


class PluginEntrypoint(PluginPatternEntrypointBase):

    def __init__(self, text, lang):
        self.is_lang_dependent = False
        super().__init__(_CWD, self.is_lang_dependent, MANIFEST["key"], lang, text)
        excl_corp_list = config_email()
        self.corp_email_class = EmailFilter(excl_corp_list)
        self.emails_entities = list()

    def filter_emails(self, total_ent_strict_list):
        for ent in total_ent_strict_list:
            if not self.corp_email_class.is_corp_email(ent[0]):
                self.emails_entities.append(ent)

    def run_pattern_detector(self):
        pattern_detector = PatternDetector(self.text, self.lang, self.get_pattern())

        total_ent_strict_list, [], [], [] = pattern_detector.get_kpis(
            self.text)

        self.filter_emails(total_ent_strict_list)

        return get_unique_ents(self.emails_entities)

    def output(self, unconsolidated_lax_dict=None, consolidated_lax_dict=None, strict_ent_dict=None,
               validate_dict=None):
        return super().output(strict_ent_dict=strict_ent_dict)

    def run(self):
        unique_strict_ent_dict = self.run_pattern_detector()
        return self.output(strict_ent_dict=unique_strict_ent_dict)
