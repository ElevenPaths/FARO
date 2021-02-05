import unittest
from pathlib import Path

from plugins.address_bitcoin.entrypoint import PluginEntrypoint, MANIFEST

CWD = Path(__file__).parent
INPUT_PATH = CWD / "data"
FILE_NAME = "document.txt"
GROUND_TRUTH_RESULT = ["1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2", "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy",
                       "bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq"]


def load_file(file_path):
    with open(INPUT_PATH / file_path, "r", encoding='utf8') as f_stream:
        return [f_stream.read().replace('\n', '')]


class AddressBitcoinTest(unittest.TestCase):

    def setUp(self):
        """ Setting up for the test """
        pass

    def tearDown(self):
        """ Cleaning up after the test """
        pass

    def test_for_address_bitcoin(self):
        text = load_file(FILE_NAME)
        address_bitcoin_plugin = PluginEntrypoint(text=text)
        plugin_data = address_bitcoin_plugin.run()
        results = list(plugin_data[MANIFEST['key']])
        self.assertTrue(len(results) == len(GROUND_TRUTH_RESULT))
        diff_list = (set(results) ^ set(GROUND_TRUTH_RESULT))
        self.assertTrue(len(diff_list) == 0)


if __name__ == '__main__':
    unittest.main()
