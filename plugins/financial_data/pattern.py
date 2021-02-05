#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from utils.pattern.pattern_base import PluginPatternBase

# Own modules for plugin

_CWD = os.path.dirname(__file__)
_ENTITY = "FINANCIAL_DATA"


class PluginPattern(PluginPatternBase):

    def strict_regexp(self):
        return {
            "STRICT_REG_IBAN_V1": r"\b[a-zA-Z]{2}[\s\-_]*[0-9]{2}([\s\-_]*[0-9]{4}){5}\b"
        }

    def lax_regexp(self):
        return {
            "BROAD_REG_IBAN_APPROX_V1": r"[a-zA-Z]{2}[\s\-_]*[0-9]{2}([\s\-_]*[0-9]{4}){5}"
        }

    def __init__(self, cwd=_CWD, lax_regexp=None, strict_regexp=None):
        lax_regexp = self.lax_regexp() if lax_regexp is None else lax_regexp
        strict_regexp = self.strict_regexp() if strict_regexp is None else strict_regexp
        super().__init__(cwd, lax_regexp, strict_regexp)
