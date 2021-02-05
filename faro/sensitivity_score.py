#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
from conf import config
from logger import logger

script_name = os.path.basename(__file__)
faro_logger = logger.Logger(logger_name=script_name, file_name=config.LOG_FILE_NAME, logging_level=config.LOG_LEVEL)


class SensitivityScorer(object):
    """ Class to obtain the score of confidentiality based on the entities extracted """

    def _check_index_surpass_min_specified(self, summary_dict, current_idx):
        # check if two or more index surpass the min specified
        above_min = 0

        for key in self.features:
            if self.features[key]['description'] in summary_dict:
                try:
                    if summary_dict[self.features[key]['description']] >= self.features[key]["sensitivity"][
                        self.sensitivity_list[current_idx]
                    ]["min"]:
                        above_min += 1
                except KeyError:
                    message = "Could not find %s in scoring computation" % key
                    faro_logger.debug(script_name, self._check_index_surpass_min_specified.__name__, message)

        if (above_min > self.sensitivity_multiple_kpis and
                current_idx < len(self.sensitivity_list) - 1):
            current_idx += 1

    def _get_ranking(self, summary_dict):
        """ Obtain the ranking from the summary of detected entities

        Keyword arguments:
        summary_dict -- dict with deteted entities (aggregated by type)

        """
        reached_min = False
        current_idx = 0

        for key in self.features:
            if self.features[key]['description'] in summary_dict:
                try:
                    while self.features[key]["sensitivity"][self.sensitivity_list[current_idx]]["max"] \
                            <= summary_dict[self.features[key]['description']]:
                        current_idx += 1
                        reached_min = True
                        # check if we are already in the max level of sensitivity
                        if current_idx == len(self.sensitivity_list) - 1:
                            break

                    if summary_dict[self.features[key]['description']] >= \
                            self.features[key]["sensitivity"][self.sensitivity_list[current_idx]]["min"]:
                        reached_min = True
                except KeyError:
                    message = "could not find %s in scoring computation" % key
                    faro_logger.debug(script_name, self._get_ranking.__name__, message)

        if reached_min:
            self._check_index_surpass_min_specified(summary_dict, current_idx)
            return self.sensitivity_list[current_idx]

        # None is not allowded (returning the lowest value in the list)
        return self.sensitivity_list[0]

    @staticmethod
    def _set_sensitivity_score(entity, result_dict, entity_dict, key, occurrence=False):
        if entity not in result_dict:
            result_dict[entity] = 0
        if occurrence:
            for token_key in entity_dict[key]:
                result_dict[entity] += entity_dict[key][token_key]
        else:
            result_dict[entity] = len(entity_dict[key])

    def get_sensitivity_score(self, entity_dict):
        """ Obtain the sensitivity score from a list of entities

        Keyword arguments:
        entity_dict -- dictionary of entities

        """
        result_dict = {}
        for key in entity_dict:
            # We normally count the number of unique values except for custom words
            occurrence = False
            if key == "CUSTOM":
                occurrence = True
            # Only include those features selected for output in the scoring overview file
            if self.features[key]["output"]:
                self._set_sensitivity_score(
                    self.features[key]["description"],
                    result_dict,
                    entity_dict,
                    key,
                    occurrence)
        result_dict["score"] = self._get_ranking(result_dict)
        return result_dict

    def __init__(self, conf):
        """ Initialization

        Keyword arguments:
        faro configuration

        """

        self.sensitivity_list = conf['sensitivity']['sensitivity_list']
        self.features = conf['entities']
        self.sensitivity_multiple_kpis = conf['sensitivity']['sensitivity_multiple_kpis']
