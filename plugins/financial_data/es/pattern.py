#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ..pattern import PluginPattern as ParentPluginPattern

from stdnum import get_cc_module

_CWD = os.path.dirname(__file__)


class PluginPattern(ParentPluginPattern):

    def validate(self, ent):
        return get_cc_module('es', 'ccc').is_valid(ent) or get_cc_module('es', 'iban').is_valid(ent)

    def __init__(self):
        super().__init__(cwd=_CWD, lax_regexp=self.lax_regexp(), strict_regexp=self.strict_regexp())
