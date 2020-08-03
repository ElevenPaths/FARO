#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from faro import ner_regex
from faro.utils import clean_text

MSG_PHONE_NOT_DETECTED = "Phone was not detected"
MSG_PHONE_DETECTED = "PHONE was detected"
MSG_PHONE_WRONG_DETECTED = "wrong phone detected"
MSG_MOBILE_NOT_DETECTED = "Mobile phone was not detected"
MSG_MOBILE_WRONG_DETECTED = "wrong mobile detected"
MSG_IBAN_NOT_DETECTED = "IBAN was not detected"
MSG_IBAN_WRONG_DETECTED = "wrong IBAN detected"
MSG_ID_DOCUMENT_NOT_DETECTED = "ID_DOCUMENT was not detected"
MSG_DNI_WRONG_DETECTED = "wrong dni detected"
MSG_NIF_WRONG_DETECTED = "wrong NIF detected"
MSG_MONEY_NOT_DETECTED = "MONEY was not detected"
MSG_CURRENCY_WRONG_DETECTED = "wrong currency detected"
MSG_EMAIL_NOT_DETECTED = "email was not detected"
MSG_EMAIL_HACK_NOT_DETECTED = "Email Hack was not detected"
MSG_EMAIL_WRONG_DETECTED = "wrong email detected"
MSG_EMAIL_HACK_DETECTED = "Wrong email Hack was detected"
MSG_CREDIT_CARD_NOT_DETECTED = "credit card was not detected"
MSG_CREDIT_CARD_DETECTED = "wrong credit card detected"
MSG_QUANTITY_DETECTED = "Wrong quantity detected"
MSG_PROB_CURRENCY_NOT_DETECTED = "PROB_CURRENCY was not detected"
MONEY_THOUSANDS = "1,000"

MSG_TEXT = "{} {} {}. Text {}"
MSG_DETECTED = "{} {}. Detected {}"
MSG_EXTRACTED = "{} {}. Extracted {}"


class NerRegexTest(unittest.TestCase):

    def setUp(self):
        """ Setting up for the test """
        pass

    def tearDown(self):
        """ Cleaning up after the test """
        pass

    def test_regexinit(self):
        """ Test the initialization of the regex detection class """
        ner_regex.RegexNer()

    def test_0_broad_phone_number_v0(self):
        """ Test the detection of a phone number """

        test = "Mi teléfono es 988 888 888 "
        ner = ner_regex.RegexNer()

        result = ner._detect_regexp(test, "broad")

        self.assertTrue("PHONE" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_PHONE_NOT_DETECTED,
                            result))

        idx = -1
        for i, _regexp in enumerate(result["PHONE"]):
            if _regexp[1] == "BROAD_REG_PHONE_NUMBER_APPROX_V3":
                idx = i
                break

        self.assertEqual(clean_text(result["PHONE"][idx][0].strip()),
                         "988888888",
                         "{self.shortDescription()} {MSG_PHONE_NOT_DETECTED}. Extracted {result['PHONE'][idx]}")

    def test_1_broad_phone_number_v0(self):
        """ Test the detection of a phone number """

        test = "Mi teléfono es +34 988 888 888 "
        ner = ner_regex.RegexNer()

        result = ner._detect_regexp(test, "broad")

        self.assertTrue("PHONE" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_PHONE_NOT_DETECTED,
                            result))

        idx = -1
        for i, _regexp in enumerate(result["PHONE"]):
            if _regexp[1] == "BROAD_REG_PHONE_NUMBER_APPROX_V3":
                idx = i
                break

        self.assertEqual(clean_text(result["PHONE"][idx][0].strip()),
                         "34988888888",
                         MSG_EXTRACTED.format(
                             self.shortDescription(),
                             MSG_PHONE_NOT_DETECTED,
                             result["PHONE"][idx]))

    def test_2_broad_phone_number_v0(self):
        """ Test the detection of a wrong phone number """

        test = "Mi teléfono es +34 988 888 888 456"
        ner = ner_regex.RegexNer()

        result = ner._detect_regexp(test, "broad")

        self.assertTrue("PHONE" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_PHONE_NOT_DETECTED,
                            result))

        for i, _regexp in enumerate(result["PHONE"]):
            if _regexp[1] == "BROAD_REG_PHONE_NUMBER_GEN_V3":
                idx = i
                break

        self.assertEqual(clean_text(result["PHONE"][idx][0].strip()),
                         "34988888888",
                         MSG_EXTRACTED.format(
                             self.shortDescription(),
                             MSG_PHONE_NOT_DETECTED,
                             result["PHONE"][idx]))

    def test_3_broad_phone_number_v0(self):
        """ Test the detection of a wrong phone number """

        test = "Mi teléfono es 45 988 888 888"
        ner = ner_regex.RegexNer()

        result = ner._detect_regexp(test, "broad")

        self.assertTrue("PHONE" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_PHONE_DETECTED,
                            result))

        for i, _regexp in enumerate(result["PHONE"]):
            if _regexp[1] == "BROAD_REG_PHONE_NUMBER_GEN_V3":
                idx = i
                break

        self.assertEqual(clean_text(result["PHONE"][idx][0].strip()),
                         "988888888",
                         MSG_EXTRACTED.format(
                             self.shortDescription(),
                             MSG_PHONE_NOT_DETECTED,
                             result["PHONE"][idx]))

    def test_0_CP_MOBILE_NUMBER_V0(self):
        """ Test the detection of a phone number """

        test = "Mi teléfono móvil es 688 888 888 "
        ner = ner_regex.RegexNer()

        result = ner._detect_regexp(test, "broad")

        self.assertTrue("MOBILE" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_MOBILE_NOT_DETECTED,
                            result))

        for i, _regexp in enumerate(result["MOBILE"]):
            if _regexp[1] == "BROAD_REG_MOBILE_NUMBER_GEN_V3":
                idx = i
                break

        self.assertEqual(clean_text(result["MOBILE"][idx][0].strip()),
                         "688888888",
                         MSG_EXTRACTED.format(
                             self.shortDescription(),
                             MSG_MOBILE_NOT_DETECTED,
                             result["MOBILE"][idx]))

    def test_1_broad_mobile_number_V0(self):
        """ Test the detection of a mobile phone number """

        test = "Mi teléfono es 45 688 888 888 "
        ner = ner_regex.RegexNer()

        result = ner._detect_regexp(test, "broad")

        self.assertTrue("MOBILE" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_MOBILE_NOT_DETECTED,
                            result))

        for i, _regexp in enumerate(result["MOBILE"]):
            if _regexp[1] == "BROAD_REG_MOBILE_NUMBER_GEN_V3":
                idx = i
                break

        self.assertEqual(clean_text(result["MOBILE"][idx][0].strip()),
                         "688888888",
                         MSG_EXTRACTED.format(
                             self.shortDescription(),
                             MSG_MOBILE_NOT_DETECTED,
                             result["MOBILE"][idx]))

    def test_2_broad_mobile_number_v0(self):
        """ Test the detection of a mobile phone number """

        test = "Mi teléfono es 45688 888 888 "
        ner = ner_regex.RegexNer()

        result = ner._detect_regexp(test, "broad")

        self.assertTrue("MOBILE" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_MOBILE_NOT_DETECTED,
                            result))

        for i, _regexp in enumerate(result["MOBILE"]):
            if _regexp[1] == "BROAD_REG_MOBILE_NUMBER_GEN_V3":
                idx = i
                break

        self.assertEqual(clean_text(result["MOBILE"][idx][0].strip()),
                         "688888888",
                         MSG_EXTRACTED.format(
                             self.shortDescription(),
                             MSG_MOBILE_NOT_DETECTED,
                             result["MOBILE"][idx]))

    def test_strict_iban_v0(self):
        """ Test the detection of the IBAN account """

        test = ("This is the IBAN of the account ES91 2100 0418 4502 " +
                "0005 1332 .")
        ner = ner_regex.RegexNer()

        result = ner._detect_regexp(test, "strict")

        self.assertTrue("FINANCIAL_DATA" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_IBAN_NOT_DETECTED,
                            result))

        idx = -1
        for i, _regexp in enumerate(result["FINANCIAL_DATA"]):
            if _regexp[1] == "STRICT_REG_IBAN_V1":
                idx = i
                break

        self.assertEqual(clean_text(result["FINANCIAL_DATA"][idx][0]),
                         "ES9121000418450200051332",
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_IBAN_WRONG_DETECTED,
                             result["FINANCIAL_DATA"][idx]))

    def test_broad_iban_V1(self):
        """ Test the detection of the IBAN account """

        test = "This is the IBAN of the account ES91 2100 4334471600021142."

        proximity_dict = {"FINANCIAL_DATA": {"left_span_len": 20,
                                            "right_span_len": 0,
                                            "word_list": ["iban"]}}

        ner = ner_regex.RegexNer(regexp_config_dict=proximity_dict)
        result = ner._detect_regexp(test, "broad")

        self.assertTrue("FINANCIAL_DATA" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_IBAN_NOT_DETECTED,
                            result))

        idx = -1
        for i, _regexp in enumerate(result["FINANCIAL_DATA"]):
            if _regexp[1] == "BROAD_REG_IBAN_APPROX_V1":
                idx = i
                break

        self.assertEqual(clean_text(result["FINANCIAL_DATA"][idx][0]),
                         "ES9121004334471600021142",
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_IBAN_WRONG_DETECTED,
                             result["FINANCIAL_DATA"][idx]))

    def test_complete_iban_V1(self):
        """ Test the detection of the IBAN account """

        test = "This is the IBAN of the account ES91 2100 4334471600021142P ."

        proximity_dict = {"FINANCIAL_DATA": {"left_span_len": 20,
                                            "right_span_len": 0,
                                            "word_list": ["iban"]}}

        ner = ner_regex.RegexNer(regexp_config_dict=proximity_dict)
        result = ner.regex_detection(test, full_text=test)

        self.assertTrue("FINANCIAL_DATA" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_IBAN_NOT_DETECTED,
                            result))

        idx = -1
        for i, _regexp in enumerate(result["FINANCIAL_DATA"]):
            if _regexp[1] == "BROAD_REG_IBAN_APPROX_V1":
                idx = i
                break

        self.assertEqual(clean_text(result["FINANCIAL_DATA"][idx][0]),
                         "ES9121004334471600021142",
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_IBAN_WRONG_DETECTED,
                             result["FINANCIAL_DATA"][idx]))

    def test_is_not_iban_V0(self):
        """ Test IBAN is not detected """

        test = ("This is the IBAN of the account ES91 2100 0418 " +
                "4502 0005 1332 4576 .")
        ner = ner_regex.RegexNer()

        result = ner._detect_regexp(test, "strict")

        self.assertTrue("FINANCIAL_DATA" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_IBAN_NOT_DETECTED,
                            result))
        idx = -1
        for i, _regexp in enumerate(result["FINANCIAL_DATA"]):
            if _regexp[1] == "BROAD_REG_IBAN_APPROX_V1":
                idx = i
                break

        self.assertEqual(clean_text(result["FINANCIAL_DATA"][idx][0]),
                         "ES9121000418450200051332",
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_IBAN_WRONG_DETECTED,
                             result["FINANCIAL_DATA"][idx]))

    def test_strict_email_v0(self):
        """ Detection of email v0 rule """

        test = "the email of John is deadbeaf@foo.bar"
        ner = ner_regex.RegexNer()
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("EMAIL" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_EMAIL_NOT_DETECTED,
                            result))

        idx = -1
        for i, _regexp in enumerate(result["EMAIL"]):
            if _regexp[1] == "STRICT_REG_EMAIL_ADDRESS_V0":
                idx = i
                break

        self.assertEqual(result["EMAIL"][idx][0], "deadbeaf@foo.bar",
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_EMAIL_WRONG_DETECTED,
                             result["EMAIL"][idx]))

    def test_strict_credit_card_v0(self):
        """ Detection of card v0 rule """

        test = "the visa card is 4111111111111111."

        ner = ner_regex.RegexNer()
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("CREDIT_CARD" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_CREDIT_CARD_NOT_DETECTED,
                            result))

        idx = -1
        for i, _regexp in enumerate(result["CREDIT_CARD"]):
            if _regexp[1] == "STRICT_REG_CREDIT_CARD_V0":
                idx = i
                break

        self.assertEqual(result["CREDIT_CARD"][idx][0], "4111111111111111",
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_CREDIT_CARD_DETECTED,
                             result["CREDIT_CARD"][idx]))

    def test_strict_dni_v0(self):
        """ Detection of DNI v0 rule """

        test = "el dni de Juan es 66666666Y."

        ner = ner_regex.RegexNer()
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("ID_DOCUMENT" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_ID_DOCUMENT_NOT_DETECTED,
                            result))

        idx = -1
        for i, _regexp in enumerate(result["ID_DOCUMENT"]):
            if _regexp[1] == "STRICT_REG_DNI_V0":
                idx = i
                break

        self.assertEqual(clean_text(result["ID_DOCUMENT"][idx][0]), "66666666Y",
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_DNI_WRONG_DETECTED,
                             result["ID_DOCUMENT"][idx]))

    def test_dni_with_dash(self):
        """ Detection of DNI v0 rule with letter separated by dash """

        test = "el dni de Juan es 66666666-Y."

        ner = ner_regex.RegexNer()
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("ID_DOCUMENT" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_ID_DOCUMENT_NOT_DETECTED,
                            result))

        idx = -1
        for i, _regexp in enumerate(result["ID_DOCUMENT"]):
            if _regexp[1] == "STRICT_REG_DNI_V0":
                idx = i
                break

        self.assertEqual(clean_text(result["ID_DOCUMENT"][idx][0]), "66666666Y",
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_DNI_WRONG_DETECTED,
                             result["ID_DOCUMENT"][idx]))

    def test_strict_dni_v1(self):
        """ Detection of DNI v0 rule with Nº stuck to the number """

        test = "el N.I.F. Nº15373458B."

        ner = ner_regex.RegexNer()
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("ID_DOCUMENT" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_ID_DOCUMENT_NOT_DETECTED,
                            result))

        idx = -1
        for i, _regexp in enumerate(result["ID_DOCUMENT"]):
            if _regexp[1] == "STRICT_REG_DNI_V0":
                idx = i
                break

        self.assertEqual(clean_text(result["ID_DOCUMENT"][idx][0]), "15373458B",
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_DNI_WRONG_DETECTED,
                             result["ID_DOCUMENT"][idx]))

    def test_strict_dni_v2(self):
        """ Detection of DNI"""

        test = "15373458B"

        ner = ner_regex.RegexNer()
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("ID_DOCUMENT" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_ID_DOCUMENT_NOT_DETECTED,
                            result))

        idx = -1
        for i, _regexp in enumerate(result["ID_DOCUMENT"]):
            if _regexp[1] == "STRICT_REG_DNI_V0":
                idx = i
                break

        self.assertEqual(clean_text(result["ID_DOCUMENT"][idx][0]), "15373458B",
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_DNI_WRONG_DETECTED,
                             result["ID_DOCUMENT"][idx]))

    def test_strict_dni_v3(self):
        """ Detection of DNI"""

        test = "15373458Bé"

        ner = ner_regex.RegexNer()
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("ID_DOCUMENT" not in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_ID_DOCUMENT_NOT_DETECTED,
                            result))

    def test_broad_phone_number_v4(self):
        """ Detection of phone number """

        test = "el teléfono de Juan es +34 986 000000"

        ner = ner_regex.RegexNer()
        result = ner._detect_regexp(test, "broad")

        self.assertTrue("PHONE" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_PHONE_NOT_DETECTED,
                            result))

        idx = -1
        for i, _regexp in enumerate(result["PHONE"]):
            if _regexp[1] == "BROAD_REG_PHONE_NUMBER_GEN_V3":
                idx = i
                break

        self.assertEqual(clean_text(result["PHONE"][idx][0]), "34986000000",
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_PHONE_WRONG_DETECTED,
                             result["PHONE"][idx]))

    def test_broad_phone_number_v5(self):
        """ Detection of phone number """

        test = "tfno.: ESP 980000001"

        ner = ner_regex.RegexNer()
        result = ner._detect_regexp(test, "broad")

        self.assertTrue("PHONE" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_PHONE_NOT_DETECTED,
                            result))

        idx = -1
        for i, _regexp in enumerate(result["PHONE"]):
            if _regexp[1] == "BROAD_REG_PHONE_NUMBER_GEN_V3":
                idx = i
                break

        self.assertEqual(clean_text(result["PHONE"][idx][0]), "980000001",
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_PHONE_WRONG_DETECTED,
                             result["PHONE"][idx]))

    def test_broad_phone_number_v6(self):
        """ Detection of phone number """

        test = "teléfono: ESP 980000001A"

        ner = ner_regex.RegexNer()
        result = ner._detect_regexp(test, "broad")

        self.assertTrue("PHONE" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_PHONE_NOT_DETECTED,
                            result))

        idx = -1
        for i, _regexp in enumerate(result["PHONE"]):
            if _regexp[1] == "BROAD_REG_PHONE_NUMBER_GEN_V3":
                idx = i
                break

        self.assertEqual(clean_text(result["PHONE"][idx][0]), "980000001",
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_PHONE_WRONG_DETECTED,
                             result["PHONE"][idx]))

    def test_complete_phone_number(self):
        """ Detection of phone number """

        test = "tel.: ESP 980000007."

        proximity_dict = {"PHONE": {
            "left_span_len": 20,
            "right_span_len": 0,
            "word_list": ["tel."]}}

        ner = ner_regex.RegexNer(regexp_config_dict=proximity_dict)
        result = ner.regex_detection(test, full_text=test)

        self.assertTrue("PHONE" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_PHONE_NOT_DETECTED,
                            result))

        self.assertEqual(clean_text(result["PHONE"][0][0]), "980000007",
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_PHONE_WRONG_DETECTED,
                             result["PHONE"][0]))

    def test_complete_phone_number_v1(self):
        """ Detection of phone number """

        test = "fax: ESP 98000000"

        proximity_dict = {"PHONE": {
            "left_span_len": 20,
            "right_span_len": 0,
            "word_list": ["tel."]}}

        ner = ner_regex.RegexNer(regexp_config_dict=proximity_dict)

        result = ner.regex_detection(test, full_text=test)

        self.assertTrue("PHONE" not in result,
                        "{} {} but it shouldn't{}".format(
                            self.shortDescription(),
                            MSG_PHONE_DETECTED,
                            result))

    def test_complete_phone_number_v2(self):
        """ Detection of phone number """

        test = "tlf.: ESP 980000000"

        proximity_dict = {"PHONE": {
            "left_span_len": 20,
            "right_span_len": 0,
            "word_list": ["tlf."]}}

        ner = ner_regex.RegexNer(regexp_config_dict=proximity_dict)

        result = ner.regex_detection(test, full_text=test)

        self.assertTrue("PHONE" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_PHONE_DETECTED,
                            result))

    def test_complete_mobile_v0(self):
        """ Detection of phone number """

        test = "móvil: ESP 780000000"

        proximity_dict = {"MOBILE": {
            "left_span_len": 20,
            "right_span_len": 0,
            "word_list": ["movil"]}}

        ner = ner_regex.RegexNer(regexp_config_dict=proximity_dict)

        result = ner.regex_detection(test, full_text=test)

        self.assertTrue("MOBILE" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_MOBILE_NOT_DETECTED,
                            result))

        self.assertEqual(clean_text(result["MOBILE"][0][0]), "780000000",
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_MOBILE_WRONG_DETECTED,
                             result["MOBILE"][0]))

    def test_generic_money_v0(self):
        """ Detection of money quantities """

        test = "el total de la factura es 1,000."

        ner = ner_regex.RegexNer()
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("PROB_CURRENCY" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_MONEY_NOT_DETECTED,
                            result))

        # search for the rule CP_MONEY_V1
        for i in range(len(result["PROB_CURRENCY"])):
            if result["PROB_CURRENCY"][i][1] == "STRICT_REG_MONEY_V1":
                idx = i

        self.assertEqual(result["PROB_CURRENCY"][idx][0], MONEY_THOUSANDS,
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_CURRENCY_WRONG_DETECTED,
                             result["PROB_CURRENCY"]))

    def test_generic_money_v1(self):
        """ Detection of money quantities """

        test = "el total de la factura es 1.000,000."

        ner = ner_regex.RegexNer()
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("PROB_CURRENCY" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_MONEY_NOT_DETECTED,
                            result))

        # search for the rule CP_MONEY_V0
        for i in range(len(result["PROB_CURRENCY"])):
            if result["PROB_CURRENCY"][i][1] == "STRICT_REG_MONEY_V0":
                idx = i

        self.assertEqual(result["PROB_CURRENCY"][idx][0], "1.000,000",
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_CURRENCY_WRONG_DETECTED,
                             result["PROB_CURRENCY"]))

    def test_generic_money_v2(self):
        """ Detection of money quantities """

        test = "el total de la factura es 1.000,000,52."

        ner = ner_regex.RegexNer()
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("PROB_CURRENCY" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_PROB_CURRENCY_NOT_DETECTED,
                            result))

        # search for the rule CP_MONEY_V0
        for i in range(len(result["PROB_CURRENCY"])):
            if result["PROB_CURRENCY"][i][1] == "STRICT_REG_MONEY_V0":
                idx = i

        self.assertEqual(result["PROB_CURRENCY"][idx][0], "1.000,000,52",
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_CURRENCY_WRONG_DETECTED,
                             result["PROB_CURRENCY"]))

    def test_generic_money_v3(self):
        """ Detection of money quantities """

        test = "el total de la factura es C42.333.333"

        ner = ner_regex.RegexNer()
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("PROB_CURRENCY" not in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_PROB_CURRENCY_NOT_DETECTED,
                            result))

    def test_generic_money_v4(self):
        """ Detection of money quantities """

        test = "el total de la factura es 1.000,000,52."

        ner = ner_regex.RegexNer()
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("PROB_CURRENCY" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_PROB_CURRENCY_NOT_DETECTED,
                            result))

        idx = -1
        # search for the rule CP_MONEY_V0
        for i in range(len(result["PROB_CURRENCY"])):
            if result["PROB_CURRENCY"][i][1] == "CP_MONEY_V1":
                idx = i

        self.assertEqual(idx, -1,
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_QUANTITY_DETECTED,
                             result["PROB_CURRENCY"]))

    def test_strict_money_euro_v0(self):
        """ Detection of euro currency """

        test = "este aparato cuesta 1,000€"

        ner = ner_regex.RegexNer()
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("MONEY" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_MONEY_NOT_DETECTED,
                            result))

        # search where euro is rules matches the sentence
        for i in range(len(result["MONEY"])):
            if result["MONEY"][i][1] == "STRICT_REG_EURO_V0":
                idx = i

        self.assertEqual(result["MONEY"][idx][0], MONEY_THOUSANDS,
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_CURRENCY_WRONG_DETECTED,
                             result["MONEY"]))

    def test_strict_money_euros_v0(self):
        """ Detection of euro currency using the word euro """

        test = "este aparato cuesta 1,000 euros"

        ner = ner_regex.RegexNer()
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("MONEY" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_MONEY_NOT_DETECTED,
                            result))

        # search where euro is rules matches the sentence
        for i in range(len(result["MONEY"])):
            if result["MONEY"][i][1] == "STRICT_REG_EURO_V0":
                idx = i

        self.assertEqual(result["MONEY"][idx][0], MONEY_THOUSANDS,
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_CURRENCY_WRONG_DETECTED,
                             result["MONEY"]))

    def test_strict_money_euros_v1(self):
        """ Detection of euro currency using the word euro """

        test = "este aparato cuesta 1000 euros"

        ner = ner_regex.RegexNer()
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("MONEY" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_MONEY_NOT_DETECTED,
                            result))

        # search where euro is rules matches the sentence
        for i in range(len(result["MONEY"])):
            if result["MONEY"][i][1] == "STRICT_REG_EURO_V0":
                idx = i

        self.assertEqual(result["MONEY"][idx][0], "1000",
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_CURRENCY_WRONG_DETECTED,
                             result["MONEY"]))

    def test_strict_money_euros_v2(self):
        """ Detection of euro currency using the word euro """

        test = "este aparato cuesta 1,000.00 euros"

        ner = ner_regex.RegexNer()
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("MONEY" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_MONEY_NOT_DETECTED,
                            result))

        # search where euro is rules matches the sentence
        for i in range(len(result["MONEY"])):
            if result["MONEY"][i][1] == "STRICT_REG_EURO_V0":
                idx = i

        self.assertEqual(result["MONEY"][idx][0], "1,000.00",
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_CURRENCY_WRONG_DETECTED,
                             result["MONEY"]))

    def test_money_CP_EURO_V0_euros_v3(self):
        """ Detection of euro currency using the word euro """

        test = "este aparato cuesta 1,000.00 Euros"

        ner = ner_regex.RegexNer()
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("MONEY" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_MONEY_NOT_DETECTED,
                            result))

        # search where euro is rules matches the sentence
        for i in range(len(result["MONEY"])):
            if result["MONEY"][i][1] == "STRICT_REG_EURO_V0":
                idx = i

        self.assertEqual(result["MONEY"][idx][0], "1,000.00",
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_CURRENCY_WRONG_DETECTED,
                             result["MONEY"]))

    def test_strict_cif_company(self):
        """ Test the detection of the CIF of the company """

        test = "El CIF de la compañía es A99151276"

        ner = ner_regex.RegexNer()
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("ID_DOCUMENT" in result,
                        "{} {} {}".format(
                            self.shortDescription(),
                            MSG_ID_DOCUMENT_NOT_DETECTED,
                            result))

        # search where euro is rules matches the sentence
        for i in range(len(result["ID_DOCUMENT"])):
            if result["ID_DOCUMENT"][i][1] == "STRICT_REG_CIF_V0":
                idx = i

        self.assertEqual(result["ID_DOCUMENT"][idx][0], "A99151276",
                         MSG_DETECTED.format(
                             self.shortDescription(),
                             MSG_NIF_WRONG_DETECTED,
                             result["ID_DOCUMENT"]))

    def test_email_hack_regex(self):
        """ Test the detection of mail hacks """

        test = "Enviar todos vuestros datos a infoAThacktextDOTcom"

        CP_EMAIL_HACK_V0 = (r"[a-zA-Z0-9_.+-]+\s?(\(|-)?\s?(AT|at)\s?(\)|-)?" +
                            "\s?[a-zA-Z0-9-]+\s?(\(|-)?\s?(DOT|dot)\s" +
                            "?(\)|-)?\s?[a-zA-Z0-9-.]+")

        HACK_REGEX = {"Email_Hack": [(CP_EMAIL_HACK_V0, "CP_EMAIL_HACK_V0")]}

        ner = ner_regex.RegexNer(strict_regexp_dict=HACK_REGEX)
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("Email_Hack" in result,
                        MSG_TEXT.format(
                            self.shortDescription(),
                            MSG_EMAIL_HACK_NOT_DETECTED,
                            result,
                            test))

        test = "Enviar todos vuestros datos a info AT hacktext DOT com"

        ner = ner_regex.RegexNer(strict_regexp_dict=HACK_REGEX)
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("Email_Hack" in result,
                        MSG_TEXT.format(
                            self.shortDescription(),
                            MSG_EMAIL_HACK_NOT_DETECTED,
                            result,
                            test))

        test = "Enviar todos vuestros datos a info (AT) hacktext (DOT) com"

        ner = ner_regex.RegexNer(strict_regexp_dict=HACK_REGEX)
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("Email_Hack" in result,
                        MSG_TEXT.format(
                            self.shortDescription(),
                            MSG_EMAIL_HACK_NOT_DETECTED,
                            result,
                            test))

        test = "Enviar todos vuestros datos a info-AT-hacktext-DOT-com"

        ner = ner_regex.RegexNer(strict_regexp_dict=HACK_REGEX)
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("Email_Hack" in result,
                        MSG_TEXT.format(
                            self.shortDescription(),
                            MSG_EMAIL_HACK_NOT_DETECTED,
                            result,
                            test))

        test = "Enviar todos vuestros datos a info-at-hacktext-dot-com"

        ner = ner_regex.RegexNer(strict_regexp_dict=HACK_REGEX)
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("Email_Hack" in result,
                        MSG_TEXT.format(
                            self.shortDescription(),
                            MSG_EMAIL_HACK_NOT_DETECTED,
                            result,
                            test))

        test = "Enviar todos vuestros datos a at-dot"

        ner = ner_regex.RegexNer(strict_regexp_dict=HACK_REGEX)
        result = ner._detect_regexp(test, "strict")

        self.assertTrue("Email_Hack" not in result,
                        MSG_TEXT.format(
                            self.shortDescription(),
                            MSG_EMAIL_HACK_DETECTED,
                            result,
                            test))


if __name__ == "__main__":
    unittest.main()
