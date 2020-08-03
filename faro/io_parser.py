#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from tika import parser, tika
import collections
import os

logger = logging.getLogger(__name__)
# Tika-python will assume the server is running and will not try to download nor start a new tika server
tika.TikaClientOnly = True

CHARS_PER_PAGE_PDF = 'pdf:charsPerPage'


def flatten(iterable):
    for el in iterable:
        if isinstance(el, collections.Iterable) and not isinstance(el, str):
            yield from flatten(el)
        else:
            yield el


def _is_run_ocr(parsed, file_size, pdf_ocr_ratio):
    #  Determine whether or not to run OCR based on the following variables
    #   - Use total number of chars recognized (pdf:charsPerPage)
    #   - Use size of file
    force_ocr = False

    if isinstance(parsed['metadata'][CHARS_PER_PAGE_PDF], list):
        chars = sum(map(int, parsed['metadata'][CHARS_PER_PAGE_PDF]))
    else:
        chars = int(parsed['metadata'][CHARS_PER_PAGE_PDF])

    if chars == 0:
        force_ocr = True
    else:
        filesize_chars_ratio = file_size / chars
        logger.debug("PDF filesize_chars_ratio: {:.2f}".format(filesize_chars_ratio))
        if filesize_chars_ratio > pdf_ocr_ratio:
            force_ocr = True
            logger.debug('size: {}, chars: {}, ratio: {}'.format(
                file_size,
                chars,
                filesize_chars_ratio))
    return force_ocr


def _run_force_ocr(parsed, file_path, request_options):
    logger.info("performing OCR on PDF file: {}".format(file_path))
    parsed['metadata']['ocr_parsing'] = True
    parsed_ocr_text = parser.from_file(
        file_path,
        service='text',
        headers={'X-Tika-PDFOcrStrategy': 'ocr_only'},
        requestOptions=request_options)
    if parsed['content'] is None:
        parsed['content'] = parsed_ocr_text['content']
    else:
        parsed['content'] += parsed_ocr_text['content']


def _smarter_strategy_ocr_pdf(parsed, disable_ocr, file_size, pdf_ocr_ratio, file_path, request_options):
    if parsed['metadata']:
        # First check if OCR is disabled by envvar
        if disable_ocr:
            return

        try:
            flat_parsed = list(flatten(parsed['metadata']['X-Parsed-By']))
            if any('TesseractOCRParser' in s for s in flat_parsed):
                # OCR already executed, return
                parsed['metadata']['ocr_parsing'] = True
                return parsed['content'], parsed['metadata']

            if parsed['metadata']['Content-Type'] == 'application/pdf':
                force_ocr = _is_run_ocr(parsed, file_size, pdf_ocr_ratio)

                if force_ocr:
                    _run_force_ocr(parsed, file_path, request_options)

        except KeyError as e:
            logger.debug("Did not find key {} in metadata".format(e))
            raise e
        except Exception as e:
            logger.error("Unexpected exception while treating PDF OCR strategy {}".format(e))
            raise e


def parse_file(file_path):
    """ Parses a file and returns the list of sentences

    Keyword arguments:
    file_path -- path to file
    threshold_filesize_chars_ratio -- filesize per char ratio in order to force OCR

    """

    # Retrieve envvars
    timeout = int(os.getenv('FARO_REQUESTS_TIMEOUT', 60))
    pdf_ocr_ratio = int(os.getenv('FARO_PDF_OCR_RATIO', 150))
    disable_ocr = os.getenv('FARO_DISABLE_OCR', False)

    # OCR is time consuming we will need to raise the request timeout to allow for processing
    request_options = {'timeout': timeout}

    # Calculate file_size
    file_size = os.path.getsize(file_path)
    parsed = {'content': None, 'metadata': None}

    try:
        parsed.update(parser.from_file(file_path, requestOptions=request_options))

        #  Add filesize to metadata:
        parsed['metadata']['filesize'] = file_size
        #  Tika adds controlled runtime errors as metadata so we need to take that into account
        if 'X-TIKA:EXCEPTION:runtime' in parsed['metadata']:
            return parsed['content'], parsed['metadata']
    except Exception as e:
        logger.error("Unexpected exception during parsing {}".format(e))
        raise e

    # try to implement a smarter strategy for OCRing PDFs
    _smarter_strategy_ocr_pdf(parsed, disable_ocr, file_size, pdf_ocr_ratio, file_path, request_options)

    return parsed['content'], parsed['metadata']
