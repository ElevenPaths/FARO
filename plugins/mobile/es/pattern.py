#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from ..pattern import PluginPattern as ParentPluginPattern

_CWD = os.path.dirname(__file__)


class PluginPattern(ParentPluginPattern):

    def strict_regexp(self):
        pass

    def lax_regexp(self):
        return {
            "BROAD_REG_MOBILE_NUMBER_GEN_V3": r"[67](\s+|-\.)?([0-9](\s+|-|\.)?){8}"
        }

    def validate(self, ent):
        pass

    def __init__(self):
        super().__init__(cwd=_CWD, lax_regexp=self.lax_regexp(), strict_regexp=self.strict_regexp())
