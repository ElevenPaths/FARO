#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ..pattern import PluginPattern as ParentPluginPattern
# Own modules for plugin
from stdnum import get_cc_module
_CWD = os.path.dirname(__file__)


class PluginPattern(ParentPluginPattern):
    def strict_regexp(self):
        return {
            "STRICT_REG_DNI_V0": r"(\b|[\(]|\bnº|\bNº)[0-9,X,M,L,K,Y][\-\. ]?[0-9]{7}[\-\. ]?[A-Z](\b|[\)\.\],:])",
            "STRICT_REG_CIF_V0": r"(\b|[\(]|\bnº|\bNº)[A-Za-z][\-\.\s]?[0-9]{2}(\.?)[0-9]{3}(\.?)[0-9]{3}(\b|[\)\.\],:])"
        }

    def lax_regexp(self):
        return {
            "BROAD_REG_DNI_GEN_V0": r"[0-9,X,M,L,K,Y][\-\. ]?[0-9]{7}[\-\. ]?[A-Z]?",
            "BROAD_REG_CIF_GEN_V0": r"[A-Za-z][\-\.\s]?[0-9]{2}([\.\-\s]?)[0-9]{3}([\-\.\s]?)[0-9]{3}"
        }

    def validate(self, ent):
        if (get_cc_module('es', 'dni').is_valid(ent) or
                get_cc_module('es', 'cif').is_valid(ent) or
                get_cc_module('es', 'nie').is_valid(ent)):
            return True
        return False

    def __init__(self):
        super().__init__(cwd=_CWD, lax_regexp=self.lax_regexp(), strict_regexp=self.strict_regexp())
