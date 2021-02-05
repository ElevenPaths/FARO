import logging
import os
from abc import ABC, abstractmethod

CWD = os.path.dirname(__file__)

logger = logging.getLogger(__name__)


def get_unique_ents(ent_list):
    """ Process the entities to obtain a json object """
    unique_ent_dict = {}
    for _ent in ent_list:
        if _ent[1] not in unique_ent_dict:
            unique_ent_dict[_ent[1]] = {}
        if _ent[0] not in unique_ent_dict[_ent[1]]:
            unique_ent_dict[_ent[1]][_ent[0]] = 0
        unique_ent_dict[_ent[1]][_ent[0]] += 1
    return unique_ent_dict


class BaseDetector(ABC):
    def __init__(self, text, lang):
        self._results = {}
        self.text = text
        self.lang = lang

    @abstractmethod
    def run(self):
        pass

    def get_results(self):
        return self._results
