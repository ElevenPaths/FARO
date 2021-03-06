#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from utils.pattern.entrypoint_pattern_base import PluginPatternEntrypointBase

_CWD = os.path.dirname(__file__)

MANIFEST = {
    "name": "Probable Currency Amount",
    "key": "PROB_CURRENCY",
    "version": "0.1",
    "type": "Currency",
    "description": "Probable Currency",
    "author": "Hugo",
    "email": "",
}


class PluginEntrypoint(PluginPatternEntrypointBase):

    def __init__(self, text, lang):
        self.is_lang_dependent = False
        super().__init__(_CWD, self.is_lang_dependent, MANIFEST["key"], lang, text)

    def output(self, unconsolidated_lax_dict=None, consolidated_lax_dict=None, strict_ent_dict=None,
               validate_dict=None):
        return super().output(strict_ent_dict=strict_ent_dict)

    def run(self):
        return super().run()
