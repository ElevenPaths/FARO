#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys
from conf import config
from langdetect import DetectorFactory
from langdetect import detect_langs
from langdetect.lang_detect_exception import LangDetectException
from logger import logger
from pathlib import Path

from utils.utils import log_exception

DetectorFactory.seed = 0

script_name = Path(__file__).name
faro_logger = logger.Logger(logger_name=script_name, file_name=config.LOG_FILE_NAME, logging_level=config.LOG_LEVEL)


def language_detection(file_lines):
    lang = "unk"
    try:
        """
            El detect no funciona correctamente.
            Detecta 'ca' en vez de 'es'
        """
        # lang = detect(" ".join(file_lines))
        # print("Detector: " + lang)
        file_lines = " ".join(file_lines)
        probabilities = detect_langs(file_lines)
        # print(probabilities)
        if probabilities:
            lang = probabilities[0].lang
        faro_logger.debug(script_name,
                          language_detection.__name__,
                          "lang: %s" % lang)
    except LangDetectException as e:
        log_exception(faro_logger, script_name, language_detection.__name__, e, sys)
    return lang
