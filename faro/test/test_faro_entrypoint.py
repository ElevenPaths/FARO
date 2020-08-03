#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import json
import argparse
import os
from os import path
from faro.faro_entrypoint import faro_execute

INPUT_FILE = 'sensitive_data.pdf'
INPUT_FILE_OCR = 'ocr.pdf'
INPUT_FILE_PROTECTED = 'protected.pdf'
INPUT_FILE_NO_METADATA = 'no_metadata.pdf'
INPUT_FILE_SPLIT_LINES = 'split_lines.docx'
INPUT_FILE_SIGNATURE = 'signature_boe.pdf'
INPUT_FILE_TESTS_TXT = 'tests.txt'
INPUT_FILE_NO_SENSITIVE = 'lorem.rtf'

CWD = os.path.dirname(__file__)
INPUT_PATH = os.path.join(CWD, 'data')
SCORE_EXT = 'score'
ENTITY_EXT = 'entity'

SIGNATURE = ['María de los Ángeles Hernández Toribio']
MONETARY_QUANTITY = ["4,99", "49,99"]
EMAILS = ["soia@telefonica.es", "test@csic.es"]
MOBILE_PHONES = ["654456654", "666444222", "651.651.651"]
DOCUMENT_ID = ["C59933143", "E-38008785", "36663760-N", "96222560J"]
FINANCIAL_DATA = ["ES6621000418401234567891", "5390700823285988", "4916697015082", "4929432390175839"]
CUSTOM_WORDS = ["confidencial", "contraseña"]

LANGUAGE_METADA = "meta:lang"


def _get_file_data(file_path):
    with open(file_path, "r") as f:
        file_text = f.read()
    return json.loads(file_text)


def _faro_run(input_path, input_file, file_type=ENTITY_EXT):
    _type = '%s.%s' % (input_file, file_type)
    params = argparse.Namespace()
    params.input_file = '%s/%s' % (input_path, input_file)
    faro_execute(params)
    faro_data = _get_file_data('%s/%s' % (input_path, _type))
    if file_type == ENTITY_EXT:
        faro_data = faro_data['entities']
    return faro_data


def _remove_output_files():
    dir_list = os.listdir(INPUT_PATH)
    for file_name in dir_list:
        try:
            if file_name.find(SCORE_EXT) != -1 or file_name.find(ENTITY_EXT) != -1:
                os.remove('%s/%s' % (INPUT_PATH, file_name))
        except FileNotFoundError:
            pass


class FaroEntrypointTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        _remove_output_files()
        cls.FARO_ENTITY_TEST_1 = _faro_run(INPUT_PATH, INPUT_FILE)

    @classmethod
    def tearDownClass(cls):
        _remove_output_files()

    def setUp(self):
        """ Setting up for the test """
        pass

    def tearDown(self):
        """ Cleaning up after the test """
        pass

    def test_document_id_detection(self):
        faro_document_ids_entity = list(self.FARO_ENTITY_TEST_1['document_id'].keys())
        self.assertTrue(len(faro_document_ids_entity) == len(DOCUMENT_ID))
        diff_list = (set(faro_document_ids_entity) ^ set(DOCUMENT_ID))
        self.assertTrue(len(diff_list) == 0)

    def test_document_financial_data_detection(self):
        faro_financial_data_entity = list(self.FARO_ENTITY_TEST_1['financial_data'].keys())
        self.assertTrue(len(faro_financial_data_entity) == len(FINANCIAL_DATA))
        diff_list = (set(faro_financial_data_entity) ^ set(FINANCIAL_DATA))
        self.assertTrue(len(diff_list) == 0)

    def test_mobile_phone_detection(self):
        faro_mobile_phone_number_entity = list(self.FARO_ENTITY_TEST_1['mobile_phone_number'].keys())
        for i in range(len(faro_mobile_phone_number_entity)):
            faro_mobile_phone_number_entity[i] = faro_mobile_phone_number_entity[i].replace(" ", "")

        self.assertTrue(len(faro_mobile_phone_number_entity) == len(MOBILE_PHONES))
        diff_list = (set(faro_mobile_phone_number_entity) ^ set(MOBILE_PHONES))
        self.assertTrue(len(diff_list) == 0)

    def test_email_detection(self):
        faro_email_entity = list(self.FARO_ENTITY_TEST_1['personal_email'].keys())
        self.assertTrue(len(faro_email_entity) == len(EMAILS))
        diff_list = (set(faro_email_entity) ^ set(EMAILS))
        self.assertTrue(len(diff_list) == 0)

    def test_monetary_quantity_detection(self):
        faro_monetary_quantity_entity = list(self.FARO_ENTITY_TEST_1['monetary_quantity'].keys())
        self.assertTrue(len(faro_monetary_quantity_entity) == len(MONETARY_QUANTITY))
        diff_list = (set(faro_monetary_quantity_entity) ^ set(MONETARY_QUANTITY))
        self.assertTrue(len(diff_list) == 0)

    def test_no_metadata(self):
        faro_no_metadata_score = _faro_run(INPUT_PATH, INPUT_FILE_NO_METADATA, SCORE_EXT)
        self.assertTrue(faro_no_metadata_score["meta:date"] is None)
        self.assertTrue(faro_no_metadata_score["meta:author"] is None)

    def test_language(self):
        faro_language_score = _faro_run(INPUT_PATH, INPUT_FILE, SCORE_EXT)
        self.assertTrue(faro_language_score[LANGUAGE_METADA] == "es")

    def test_unsupported_language(self):
        faro_language_score = _faro_run(INPUT_PATH, INPUT_FILE_PROTECTED, SCORE_EXT)
        self.assertTrue(faro_language_score[LANGUAGE_METADA] == "unk")

    def test_unsupported_language(self):
        faro_language_score = _faro_run(INPUT_PATH, INPUT_FILE_TESTS_TXT, SCORE_EXT)
        self.assertTrue(faro_language_score[LANGUAGE_METADA] == "ca")

    def test_protected_document(self):
        faro_protected_score = _faro_run(INPUT_PATH, INPUT_FILE_PROTECTED, SCORE_EXT)
        self.assertTrue(faro_protected_score["meta:encrypted"] == 1)

    def test_params_rename_output_files(self):
        entity_file_name = 'test_entity'
        score_file_name = 'test_score'

        params = argparse.Namespace()
        params.input_file = '%s/%s' % (INPUT_PATH, INPUT_FILE)
        params.output_entity_file = '%s/%s.%s' % (INPUT_PATH, entity_file_name, ENTITY_EXT)
        params.output_score_file = '%s/%s.%s' % (INPUT_PATH, score_file_name, SCORE_EXT)
        faro_execute(params)

        self.assertTrue(path.exists(params.output_entity_file))
        self.assertTrue(path.exists(params.output_score_file))

    def test_params_verbose(self):
        entity_file_name = 'test_verbose_entity'
        score_file_name = 'test_verbose_score'

        params = argparse.Namespace()
        params.input_file = '%s/%s' % (INPUT_PATH, INPUT_FILE)
        params.output_entity_file = '%s/%s.%s' % (INPUT_PATH, entity_file_name, ENTITY_EXT)
        params.output_score_file = '%s/%s.%s' % (INPUT_PATH, score_file_name, SCORE_EXT)
        params.verbose = True
        faro_execute(params)

        faro_verbose = _get_file_data(params.output_entity_file)
        faro_verbose_entity = faro_verbose['entities']

        self.assertTrue(faro_verbose_entity['person'] is not None)
        self.assertTrue(faro_verbose_entity['phone_number'] is not None)
        self.assertTrue(faro_verbose_entity['probable_currency_amount'] is not None)

    def test_params_split_lines(self):
        params = argparse.Namespace()
        params.input_file = '%s/%s' % (INPUT_PATH, INPUT_FILE_SPLIT_LINES)
        params.split_lines = True
        faro_execute(params)

        faro_split_lines = _get_file_data(params.output_entity_file)
        faro_split_lines_entity = faro_split_lines['entities']

        self.assertTrue(faro_split_lines_entity.get('mobile_phone_number') is None)

    def test_ocr(self):
        faro_ocr = _faro_run(INPUT_PATH, INPUT_FILE_OCR)
        faro_ocr_financial_data = list(faro_ocr['financial_data'].keys())
        self.assertTrue(len(faro_ocr_financial_data) == len(FINANCIAL_DATA))
        diff_list = (set(faro_ocr_financial_data) ^ set(FINANCIAL_DATA))
        self.assertTrue(len(diff_list) == 0)

    def test_signature(self):
        faro_signature_score = _faro_run(INPUT_PATH, INPUT_FILE_SIGNATURE, SCORE_EXT)['signature']
        faro_signature_entity = _get_file_data(os.path.join(INPUT_PATH, INPUT_FILE_SIGNATURE + "." + ENTITY_EXT))
        faro_signature_entity = list(faro_signature_entity['entities']['signature'])
        self.assertTrue(faro_signature_score == 1)
        self.assertTrue(faro_signature_entity[0] == SIGNATURE[0])

    def test_custom_words(self):
        faro_custom_score = _faro_run(INPUT_PATH, INPUT_FILE_TESTS_TXT, SCORE_EXT)['custom_words']
        faro_custom_entity = _get_file_data(os.path.join(INPUT_PATH, INPUT_FILE_TESTS_TXT + "." + ENTITY_EXT))
        faro_entities = list(faro_custom_entity['entities']['custom_words'])
        self.assertTrue(faro_custom_score == 2)
        diff_list = (set(faro_entities) ^ set(CUSTOM_WORDS))
        self.assertTrue(len(diff_list) == 0)

    def test_corp_emails(self):
        entity_file_name = 'test_corp_email_entity'
        score_file_name = 'test_corp_email_score'

        params = argparse.Namespace()
        params.input_file = '%s/%s' % (INPUT_PATH, INPUT_FILE_TESTS_TXT)
        params.output_entity_file = '%s/%s.%s' % (INPUT_PATH, entity_file_name, ENTITY_EXT)
        params.output_score_file = '%s/%s.%s' % (INPUT_PATH, score_file_name, SCORE_EXT)
        params.verbose = True
        faro_execute(params)

        faro_entities = _get_file_data(params.output_entity_file)['entities']
        self.assertTrue(faro_entities['corporate_email'] is not None)
        self.assertEqual(len(faro_entities['corporate_email']), 2)

    def test_no_sensitive_data(self):
        faro_custom_score = _faro_run(INPUT_PATH, INPUT_FILE_NO_SENSITIVE, SCORE_EXT)['score']
        faro_custom_entity = _get_file_data(os.path.join(INPUT_PATH, INPUT_FILE_NO_SENSITIVE + "." + ENTITY_EXT))
        faro_entities = list(faro_custom_entity['entities'])
        self.assertTrue(faro_custom_score == "low")
        self.assertTrue(len(faro_entities) == 0)


if __name__ == "__main__":
    unittest.main()
