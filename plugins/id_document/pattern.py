#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# Own modules for plugin

from utils.pattern.pattern_base import PluginPatternBase

_CWD = os.path.dirname(__file__)


class PluginPattern(PluginPatternBase):

    def strict_regexp(self):
        pass

    def lax_regexp(self):
        pass

    def validate(self, ent):
        pass

    def __init__(self, cwd=_CWD, lax_regexp=None, strict_regexp=None):
        lax_regexp = self.lax_regexp() if lax_regexp is None else lax_regexp
        strict_regexp = self.strict_regexp() if strict_regexp is None else strict_regexp
        super().__init__(cwd, lax_regexp, strict_regexp)
