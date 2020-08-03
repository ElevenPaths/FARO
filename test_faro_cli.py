#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest
import subprocess

CWD = os.path.dirname(__file__)
INPUT_PATH = os.path.join(CWD, 'faro/test/data')
INPUT_FILE = 'sensitive_data.pdf'
INPUT_SCORE_FILE = '%s.score' % INPUT_FILE
INPUT_ENTITY_FILE = '%s.entity' % INPUT_FILE

DUMP_DATA = ["sensitive_data.pdf", "high", "2,0,2,3,4,4,0", "application/pdf", "ENRIQUE ANDRADE GONZALEZ"]


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
        subprocess.run(['./faro_detection.py', '-i', input_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertTrue(os.path.isfile('%s/%s' % (INPUT_PATH, INPUT_ENTITY_FILE)))

    def test_faro_detection_dump(self):
        input_file = '%s/%s' % (INPUT_PATH, INPUT_FILE)
        result = subprocess.Popen(['./faro_detection.py', '-i', input_file, "--dump"], stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        out, err = result.communicate()
        out = out.decode('utf-8')

        for chain in DUMP_DATA:
            position = out.find(chain)
            self.assertTrue(position!=-1)


if __name__ == "__main__":
    unittest.main()
