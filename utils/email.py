#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from conf import config
from logger import logger

script_name = os.path.basename(__file__)
faro_logger = logger.Logger(logger_name=script_name, file_name=config.LOG_FILE_NAME, logging_level=config.LOG_LEVEL)


class EmailFilter(object):

    def is_corp_email(self, email):
        """ Detect if an email is not corporative

        Keyword arguments:
        email -- the first part on an email (before the @)

        """

        email_parts = email.split("@")

        if self.excl_corp_list is not None:
            # search for corporative mail in list
            for _corp in self.excl_corp_list:
                if email_parts[0] == _corp:
                    return True

        # searching for corporative mails of the type <company>@<company>.com
        if fuzz.ratio(email_parts[0], email_parts[1].split(".")[0]) > self.fuzziness:
            return True

        # fuzzy searching for similar corporative mails
        _choice = process.extractOne(
            email_parts[0], self.excl_corp_list, scorer=fuzz.ratio)
        # returns candidate and ratio, we choose the ratio to check against threshold
        if _choice[1] > self.fuzziness:
            return True

        return False

    def __init__(self, excl_corp_list=None):
        """ Initalization

        Keyword arguments:
        email_model -- a model that detects corporative emails

        """
        self.excl_corp_list = excl_corp_list
        self.fuzziness = 90
