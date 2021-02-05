#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from stdnum.bitcoin import is_valid

from utils.pattern.pattern_base import PluginPatternBase

_CWD = os.path.dirname(__file__)


class PluginPattern(PluginPatternBase):
    """
    Main plugin pattern class.

    """

    def strict_regexp(self):
        """
        Strict regexp method.

        :return: Dictionary with n strict regexp expressions such as

        {
            "NAME_V0": r"strict_regex expresion_0",
            "NAME_V1": r"strict_regex_expresion_1",
            ...
            "NAME_Vn": r"strict_regex_expresion_n"
        }

        """
        return {
            "STRICT_REG_BITCOIN_P2PKH_P2SH_V0": r"[13][a-km-zA-HJ-NP-Z0-9]{26,33}",
            "STRICT_REG_BITCOIN_BECH32_V0": r"(bc1)[a-zA-HJ-NP-Z0-9]{25,39}"

        }

    def lax_regexp(self):
        """
        Lax regexp method.

        :return: Dictionary with n lax regexp expressions such as

        {
            "NAME_V0": r"lax_regex expresion_0",
            "NAME_V1": r"lax_regex_expresion_1",
            ...
            "NAME_Vn": r"lax_regex_expresion_n"
        }

        """
        pass

    def validate(self, ent):
        """
        Validate detected entities.

        :param ent: Input entity
        :return: Return whether (True) or not (False) entity is being validated.
        """
        return is_valid(ent)

    def __init__(self, cwd=_CWD, lax_regexp=None, strict_regexp=None):
        lax_regexp = self.lax_regexp() if lax_regexp is None else lax_regexp
        strict_regexp = self.strict_regexp() if strict_regexp is None else strict_regexp
        super().__init__(cwd, lax_regexp, strict_regexp)
