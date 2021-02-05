#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import datetime
import io
import json
import sys
import time
from pathlib import Path

import yaml
from langdetect import DetectorFactory

from conf import config
from faro.document import FARODocument
from faro.language.language_detection import language_detection
from faro.sensitivity_score import SensitivityScorer
from logger import logger
from plugins.orchestrator import Orchestrator

CWD = Path(__file__).parent.parent
CONFIG_PATH = CWD / "conf"
_COMMONS_YAML = CONFIG_PATH / "commons.yaml"

ACCEPTED_LANGS = ["es"]
# init the seeed of the lang detection algorithm
DetectorFactory.seed = 0

script_name = Path(__file__).name
faro_logger = logger.Logger(logger_name=script_name, file_name=config.LOG_FILE_NAME, logging_level=config.LOG_LEVEL)


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

    if not hasattr(params, 'filehash'):
        params.filehash = None
    return params


def _generate_entities_output(entities, params, conf):
    """
    Generate entities output humanizing feature descriptions
    """
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    if not params.verbose:
        # Dict comprehension to filter out not verbose output
        filtered_entities = {k: v for k,
                                      v in entities.items() if conf["entities"][k]["output"] == True}
    else:
        filtered_entities = entities

    output_entities = {conf["entities"][k]["description"]: v for k,
                                                                 v in filtered_entities.items()}

    entity_dict = {"filepath": params.input_file,
                   "entities": output_entities,
                   "datetime": st}
    return entity_dict


def _persist_entities_output(entity_dict, params):
    """
    Persist detected entities to disk
    """
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


def _generate_scoring_output(result, params, conf, faro_doc):
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
    header.extend(conf["spider_output_entities"])
    # Add document metadata
    header.extend(faro_doc.get_metadata().keys())
    writer = csv.DictWriter(sys.stdout, fieldnames=header,
                            extrasaction='ignore', restval=0)
    result["id_file"] = params.input_file
    message = "JSON (Entities detected) {}".format(
        json.dumps(result, ensure_ascii=False))
    faro_logger.debug(script_name,
                      _generate_scoring_output.__name__,
                      message)
    writer.writerow(result)


def faro_execute(params):
    """ Execution of the main loop """
    # Validate params
    params = _check_input_params(params)
    # reading commons configuration
    with open(_COMMONS_YAML, "r", encoding='utf8') as f_stream:
        commons_config = yaml.load(f_stream, Loader=yaml.FullLoader)

    # parse input file and join sentences if requested
    message = "Analysing {}".format(params.input_file)
    faro_logger.info(script_name, faro_execute.__name__, message)

    # Initialize our document representation
    faro_doc = FARODocument(params.input_file, params.split_lines)
    # Parse document and extract content and metadata
    faro_doc.parse_document_data()

    # Language customization
    lang = language_detection(faro_doc.content)
    faro_doc.set_language(lang)
    lang = {"lang": lang}

    # joining two dicts with configurations
    # config becomes a shallowly merged dictionary with values from commons_config
    # replacing those from config
    conf = {**lang, **commons_config}

    faro_logger.debug(script_name, faro_execute.__name__, "Running plug-ins")
    orchestrator = Orchestrator(conf)
    entities_dict = orchestrator.run_plugins(str(faro_doc.content))

    # Initialize our scoring class
    scorer = SensitivityScorer(conf)

    # score the document, given the extracted entities
    scoring = _compute_scoring(scorer, entities_dict, faro_doc)

    # output
    result = _generate_entities_output(entities_dict, params, conf)

    faro_logger.debug(script_name, faro_execute.__name__, str(entities_dict))
    faro_logger.debug(script_name, faro_execute.__name__, str(result))

    _persist_entities_output(result, params)
    _generate_scoring_output(scoring, params, conf, faro_doc)
