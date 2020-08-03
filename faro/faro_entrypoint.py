#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import io
import os
import sys
import csv
import yaml
import json
import time
import datetime
from langdetect import detect
from langdetect import DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from faro.detector import Detector
from faro.sensitivity_score import SensitivityScorer
from .document import FARODocument

CWD = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(CWD, '..', 'config')
MODELS_PATH = os.path.join(CWD, '..', 'models')
_COMMONS_YAML = "%s/commons.yaml" % CONFIG_PATH

ACCEPTED_LANGS = ["es"]
# init the seeed of the lang detection algorithm
DetectorFactory.seed = 0

logger = logging.getLogger(__name__)


def _check_input_params(params):
    """
    Validate default params useful for unit testing
    """
    if not hasattr(params, 'output_score_file'):
        params.output_score_file = "{}{}".format(params.input_file, ".score")

    if not hasattr(params, 'output_entity_file'):
        params.output_entity_file = "{}{}".format(params.input_file, ".entity")

    if not hasattr(params, 'split_lines'):
        params.split_lines = False

    if not hasattr(params, 'verbose'):
        params.verbose = False

    if not hasattr(params, 'dump'):
        params.dump = False
    return params


def _customize_faro_engine_by_language(lang):
    # TODO: refactor code, we need to simplify the flow since docs with no content
    # go through a lot of unnecessary processing
    if lang in ACCEPTED_LANGS:
        with open("%s/%s.%s" % (CONFIG_PATH, lang, "yaml"), "r") as stream:
            config = yaml.load(stream, Loader=yaml.FullLoader)

    else:
        logger.debug("Language {} is not fully supported. All the " +
                     "functionality is only implemented for these languages: {}".format(
                         lang, " ".join(ACCEPTED_LANGS)))

        with open("%s/nolanguage.%s" % (CONFIG_PATH, "yaml"), "r") as stream:
            config = yaml.load(stream, Loader=yaml.FullLoader)
    return config


def _generate_entities_output(entities, params, config):
    """
    Generate entities output humanizing feature descriptions
    """
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    if not params.verbose:
        # Dict comprehension to filter out not verbose output
        filtered_entities = {k: v for k,
                                      v in entities.items() if config["features"][k]["output"] == True}
    else:
        filtered_entities = entities

    output_entities = {config["features"][k]["description"]: v for k,
                                                                   v in filtered_entities.items()}

    entity_dict = {"filepath": params.input_file,
                   "entities": output_entities,
                   "datetime": st}
    with io.open(params.output_entity_file, "a+") as f_out:
        f_out.write("{}\n".format(json.dumps(entity_dict, ensure_ascii=False)))


def _compute_scoring(scorer, entities, faro_doc):
    result = scorer.get_sensitivity_score(entities)
    # update score if error in reading metatada is found
    if hasattr(faro_doc, "metadata_error"):
        result["score"] = "error"

    # Force encrypted files to be considered as high
    try:
        if faro_doc.encrypted == 1:
            result["score"] = "high"
    except AttributeError:
        pass
    return result


def _generate_scoring_output(result, params, config, faro_doc):
    # Adding metadata to output
    result.update(faro_doc.get_metadata())

    if not params.dump:
        with open(params.output_score_file, "w") as f_out:
            f_out.write("{}\n".format(
                json.dumps(result, ensure_ascii=False)))
        return

    # Create list with output fieldnames
    header = ["id_file", "score"]
    #  Add all sensitive info categories
    header.extend(config["scoring_output_features"])
    # Add document metadata
    header.extend(faro_doc.get_metadata().keys())
    writer = csv.DictWriter(sys.stdout, fieldnames=header,
                            extrasaction='ignore', restval=0)
    result["id_file"] = params.input_file
    logging.debug("JSON (Entities detected) {}".format(
        json.dumps(result, ensure_ascii=False)))
    writer.writerow(result)


def language_detection(file_lines):
    try:
        lang = detect(" ".join(file_lines))
    except LangDetectException:
        lang = "unk"
    return lang


def faro_execute(params):
    """ Execution of the main loop """
    # Validate params
    params = _check_input_params(params)
    # reading commons configuration
    with open(_COMMONS_YAML, "r") as f_stream:
        commons_config = yaml.load(f_stream, Loader=yaml.FullLoader)

    # parse input file and join sentences if requested
    logger.info("Analysing {}".format(params.input_file))

    # Initialize our document representation
    faro_doc = FARODocument(params.input_file, params.split_lines)
    # Parse document and extract content and metadata
    faro_doc.get_document_data()

    # Language customization
    lang = language_detection(faro_doc.content)
    faro_doc.set_language(lang)
    config = _customize_faro_engine_by_language(lang)

    # joining two dicts with configurations
    # config becomes a shallowly merged dictionary with values from commons_config
    #  replacing those from config
    config = {**config, **commons_config}

    # instantiate detector with current configuration
    my_detector = Detector(config)
    # Detect features in the document content
    entities_dict = my_detector.analyse(faro_doc.content)

    # Initialize our scoring class
    scorer = SensitivityScorer(config)
    # score the document, given the extracted entities
    result = _compute_scoring(scorer, entities_dict, faro_doc)

    # output
    _generate_entities_output(entities_dict, params, config)
    _generate_scoring_output(result, params, config, faro_doc)
