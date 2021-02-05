#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


def log_exception(logger_exceptions, filename, method, exception, system_info):
    if system_info is not None:
        exc_type, exc_obj, exc_tb = system_info.exc_info()
        error_msg = "Error: " + str(exception) + ". Line: " + str(exc_tb.tb_lineno)
        logger_exceptions.error(filename, method, error_msg)
    else:
        logger_exceptions.error(filename, method, str(exception))


def normalize_text(message):
    """ Clean text of dots between chars

    Keyword arguments:
    message -- a plain sentence or paragraph

    """

    sent = message.lower()
    sent = sent.replace("á", "a")
    sent = sent.replace("é", "e")
    sent = sent.replace("í", "i")
    sent = sent.replace("ó", "o")
    sent = sent.replace("ú", "u")
    sent = re.sub(r'(?i)(?<=[a-z])\.(?=[a-z])', "", sent)

    return sent


def clean_text(message):
    """ Delete extra characters from text before validation

    Keyword arguments:
    message -- a plain sentence or paragraph

    """

    sent = re.sub(r'[\-_*+,\(\).:]{1,}', "", message)
    sent = re.sub(r'[ ]{1,}', "", sent)
    sent = re.sub(r'(?i)\bnº', "", sent)

    return sent


def preprocess_text(message):
    """ Delete some artifacts from text

    Keyword arguments:
    message -- a plain sentence or paragraph

    """
    return message.replace("\t", " ").replace("\r\n", " ").replace("\r", " ").replace("\n", " ")


def preprocess_file_content(content, split_lines):
    """ Do some preprocessing to clean tika output

     Keyword arguments:
    file_lines: list of text lines extracted with Tika
    join_lines: should lines be joined (e.g. a paragraph)
    """

    if content is not None:
        lines = content.strip().split("\n")
    else:
        return []

    if split_lines:
        file_lines = [preprocess_text(line) for line in lines]
    else:
        #  Combine lines
        file_lines = [" ".join([preprocess_text(line) for line in lines])]

    return file_lines
