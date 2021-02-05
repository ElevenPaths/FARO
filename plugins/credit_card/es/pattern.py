#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from ..pattern import PluginPattern as ParentPluginPattern

_CWD = os.path.dirname(__file__)


class PluginPattern(ParentPluginPattern):

    def __init__(self):
        super().__init__(cwd=_CWD, lax_regexp=self.lax_regexp(), strict_regexp=self.strict_regexp())
