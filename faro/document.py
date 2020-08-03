#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from .utils import preprocess_file_content
from .io_parser import parse_file
from collections import OrderedDict

META_AUTHOR = "meta:author"
META_CONTENT_TYPE = "meta:content-type"
META_ENCRYPTED = "meta:encrypted"
META_PAGES = "meta:pages"
META_LANGUAGE = "meta:lang"
META_DATE = "meta:date"
META_FILE_SIZE = "meta:filesize"
META_OCR = "meta:ocr"

logger = logging.getLogger(__name__)


def _assign_author_metadata(metadata):
    author = None
    if "Author" in metadata:
        author = metadata["Author"]
    elif META_AUTHOR in metadata:
        author = metadata[META_AUTHOR]
    elif "creator" in metadata:
        author = metadata["creator"]

    elif "dc:creator" in metadata:
        author = metadata["dc:creator"]

    elif "pdf:docinfo:creator" in metadata:
        author = metadata["pdf:docinfo:creator"]

    elif "producer" in metadata:
        author = metadata["producer"]

    elif "pdf:docinfo:producer" in metadata:
        author = metadata["pdf:docinfo:producer"]
    return author


def _assign_number_pages_metadata(metadata):
    if "xmpTPg:NPages" in metadata:
        num_of_pages = metadata["xmpTPg:NPages"]

    elif "Page-Count" in metadata:
        num_of_pages = metadata["Page-Count"]

    elif "meta:page-count" in metadata:
        num_of_pages = metadata["meta:page-count"]

    else:
        # not supported yet (we consider the document as one page)
        num_of_pages = 1

    if isinstance(num_of_pages, list):
        num_of_pages = sum([int(num_pages) for num_pages in num_of_pages])

    return num_of_pages


def _assign_creation_date_metadata(metadata):
    creation_date = None
    if "Creation-Date" in metadata:
        creation_date = metadata["Creation-Date"]

    elif "meta:creation_date" in metadata:
        creation_date = metadata["meta:creation_date"]

    elif "created" in metadata:
        creation_date = metadata["created"]

    if isinstance(creation_date, list):
        creation_date = creation_date[0]
    return creation_date


def _assign_content_type_metadata(metadata):
    if isinstance(metadata["Content-Type"], list):
        content_type = str(metadata["Content-Type"][0])
    else:
        content_type = metadata["Content-Type"]
    return content_type


def _assign_encrypted_metadata(metadata):
    encrypted = 0
    key = 'X-TIKA:EXCEPTION:runtime'
    if key in metadata and 'EncryptedDocumentException' in metadata[key]:
        encrypted = 1
    return encrypted


def _assign_file_size_metadata(metadata):
    file_size = None
    if "filesize" in metadata:
        file_size = metadata["filesize"]
    return file_size


def _assign_ocr_parsing_metadata(metadata):
    ocr_parsing = 0
    if "ocr_parsing" in metadata:
        ocr_parsing = 1
    return ocr_parsing


class FARODocument(object):
    """ Class to store information of the faro documents in an homogeneous format

    The current information per document is:
    - lang -- language detected
    - num_of_pages -- number of pages in the document
    - content_type -- type of content of the document

    """

    def set_language(self, language):
        """ Set language for the document provided by langdetect library"""
        self.lang = language

    def get_metadata(self):
        """ Extract a dictionary with metadata"""

        dict_result = OrderedDict()

        # Adding metadata of fyle type to output
        dict_result[META_CONTENT_TYPE] = getattr(self, "content_type", None)
        dict_result[META_ENCRYPTED] = getattr(self, "encrypted", None)
        dict_result[META_AUTHOR] = getattr(self, "author", None)
        dict_result[META_PAGES] = getattr(self, "num_of_pages", None)
        dict_result[META_LANGUAGE] = getattr(self, "lang", None)
        dict_result[META_DATE] = getattr(self, "creation_date", None)
        dict_result[META_FILE_SIZE] = getattr(self, "filesize", None)
        dict_result[META_OCR] = getattr(self, "ocr_parsing", None)

        return dict_result

    def _parse_metadata(self, metadata):
        """ Extract relevant document metadata from a tika metadata dict

        Keyword arguments:
        meta_dict -- dict of metadata (as returned by tika)

        """
        logger.debug("METADATA DICT {}".format(metadata))

        if metadata is None:
            self.metadata_error = True
            return

        # extract content type
        self.content_type = _assign_content_type_metadata(metadata)

        # detect encrypted docs
        self.encrypted = _assign_encrypted_metadata(metadata)

        # pick author
        self.author = _assign_author_metadata(metadata)

        # number of pages
        self.num_of_pages = _assign_number_pages_metadata(metadata)

        self.filesize = _assign_file_size_metadata(metadata)

        # OCRed
        self.ocr_parsing = _assign_ocr_parsing_metadata(metadata)

        # Creation date
        self.creation_date = _assign_creation_date_metadata(metadata)

    def get_document_data(self):
        """
        Launch tika parser and retrieve both content and metadata
        """
        # parse input file and join sentences if requested
        try:
            tika_content, tika_metadata = parse_file(self.document_path)
        except Exception:
            tika_content = ""
            tika_metadata = None

        self.content = preprocess_file_content(tika_content, self.split_lines)
        self._parse_metadata(tika_metadata)

    def __init__(self, document_path, split_lines):
        """ Initialization

        Keyword arguments:
        document_path -- path to the document
        split_lines -- wether to split lines or not

        """
        # store the document path
        self.document_path = document_path
        # store wether or not we should split lines or not
        self.split_lines = split_lines
