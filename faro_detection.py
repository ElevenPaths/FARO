#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path

from conf import config
from faro.faro_entrypoint import faro_execute
from logger import logger

script_name = Path(__file__).name
faro_logger = logger.Logger(logger_name=script_name, file_name=config.LOG_FILE_NAME, logging_level=config.LOG_LEVEL)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Decoder params
    parser.add_argument('--input_file', '-i', dest="input_file",
                        type=str, default=None, required=True,
                        help='Input file ')
    parser.add_argument('--output_entity_file', dest="output_entity_file",
                        type=str, default=None,
                        help=('Json file with detected entities ' +
                              '(defaults: $INPUT_FILE.entity)'))
    parser.add_argument('--output_score_file',
                        dest="output_score_file",
                        type=str, default=None,
                        help=('Json with sensitivity score and ' +
                              'summary information ' +
                              '(defaults: $INPUT_FILE.score)'))
    parser.add_argument('--split_lines', dest="split_lines",
                        action="store_true", default=False,
                        help=("Do not join sentences of a document " +
                              " (use only if every line in the document " +
                              "is already line in the document " +
                              "(e.g. a raw text file) " +
                              "(defaults: %(default)s)"))
    parser.add_argument('--verbose', dest="verbose",
                        action="store_true", default=False,
                        help=("Store all entities in json " +
                              "(defaults: %(default)s)"))
    parser.add_argument('--dump', dest="dump",
                        action="store_true", default=False,
                        help=("Dump information to stdout instead of file" +
                              "(defaults: %(default)s"))
    params = parser.parse_args()
    if params.output_entity_file is None:
        params.output_entity_file = "{}{}".format(params.input_file, ".entity")
    if params.output_score_file is None:
        params.output_score_file = "{}{}".format(params.input_file, ".score")

    faro_execute(params)
