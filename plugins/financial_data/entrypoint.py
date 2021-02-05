#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from utils.pattern.entrypoint_pattern_base import PluginPatternEntrypointBase

_CWD = os.path.dirname(__file__)

MANIFEST = {
    "name": "Financial Data",
    "key": "FINANCIAL_DATA",
    "version": "0.1",
    "type": "Financial",
    "description": "Financial Data",
    "author": "Enrique",
    "email": "enrique@telefonica.com",
}


class PluginEntrypoint(PluginPatternEntrypointBase):

    def __init__(self, text, lang):
        self.is_lang_dependent = True
        super().__init__(_CWD, self.is_lang_dependent, MANIFEST["key"], lang, text)

    def output(self, unconsolidated_lax_dict=None, consolidated_lax_dict=None, strict_ent_dict=None,
               validate_dict=None):
        return super().output(validate_dict=validate_dict)

    def run(self):
        return super().run()
