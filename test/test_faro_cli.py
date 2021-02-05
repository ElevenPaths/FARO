#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest
import subprocess
from pathlib import Path

CWD = Path(__file__).parent
INPUT_PATH = CWD / "data"
INPUT_FILE = 'sensitive_data.pdf'
INPUT_SCORE_FILE = '%s.score' % INPUT_FILE
INPUT_ENTITY_FILE = '%s.entity' % INPUT_FILE
FARO_DETECTION_PATH = CWD.parent / 'faro_detection.py'

DUMP_DATA = ["sensitive_data.pdf", "high", "2,0,2,3,5,4,0", "application/pdf", "ENRIQUE ANDRADE GONZALEZ"]


class FaroCommandLineTest(unittest.TestCase):

    def setUp(self):
        """ Setting up for the test """
        pass

    def tearDown(self):
        """ Cleaning up after the test """
        try:
            os.remove('%s/%s' % (INPUT_PATH, INPUT_SCORE_FILE))
            os.remove('%s/%s' % (INPUT_PATH, INPUT_ENTITY_FILE))
        except FileNotFoundError:
            pass

    def test_faro_detection_file(self):
        input_file = '%s/%s' % (INPUT_PATH, INPUT_FILE)
        subprocess.run([FARO_DETECTION_PATH, '-i', input_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertTrue(os.path.isfile('%s/%s' % (INPUT_PATH, INPUT_ENTITY_FILE)))

    def test_faro_detection_dump(self):
        input_file = '%s/%s' % (INPUT_PATH, INPUT_FILE)
        result = subprocess.Popen([FARO_DETECTION_PATH, '-i', input_file, "--dump"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        out, err = result.communicate()
        out = out.decode('utf-8')

        for chain in DUMP_DATA:
            position = out.find(chain)
            self.assertTrue(position != -1)


if __name__ == "__main__":
    unittest.main()
