#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from stdnum.luhn import is_valid

from utils.pattern.pattern_base import PluginPatternBase

# Own modules for plugin

_CWD = os.path.dirname(__file__)


class PluginPattern(PluginPatternBase):

    def strict_regexp(self):
        return {
            "STRICT_REG_CREDIT_CARD_V0": r"(?:(?P<visa>((?<![0-9])(?<![0-9][,.]))4[0-9]{12}(?:[0-9]{3})?)|(?P<mastercard>((?<![0-9])(?<![0-9][,.]))5[1-5][0-9]{14})|(?P<discover>((?<![0-9])(?<![0-9][,.]))6(?:011|5[0-9][0-9])[0-9]{12}))"
        }

    def lax_regexp(self):
        return {"BROAD_REG_CREDIT_CARD_GEN_V1": r"([0-9][\s\-_\.]*){8,}"}

    def validate(self, ent):
        try:
            return (12 < len(ent) < 20) and is_valid(ent)
        except:
            return False

    def __init__(self, cwd=_CWD, lax_regexp=None, strict_regexp=None):
        lax_regexp = self.lax_regexp() if lax_regexp is None else lax_regexp
        strict_regexp = self.strict_regexp() if strict_regexp is None else strict_regexp
        super().__init__(cwd, lax_regexp, strict_regexp)
        # print("Pattern Generico")
