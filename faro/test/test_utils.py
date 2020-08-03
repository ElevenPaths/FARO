#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from faro import utils

class UtilsTest(unittest.TestCase):

    def setUp(self):
        """ Setting up for the test """
        pass

    def tearDown(self):
        """ Cleaning up after the test """
        pass

    def test_normalize_text_v0(self):
        """ Test the normalization to find words in the proximity """

        message = "este es mi N.I.F.: 4576889J"

        norm_text = utils.normalize_text(message)

        self.assertEqual(norm_text, "este es mi nif.: 4576889j",
                         "{} Normalized text is not the expected result {}".format(
                             self.shortDescription(),
                             norm_text))

if __name__ == "__main__":
    unittest.main()
