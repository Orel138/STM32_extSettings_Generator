import unittest
from src.extSettingsManager import ExtSettingsManager
import os
import json


class TestExtSettingsManager(unittest.TestCase):

    def setUp(self):
        # Setup test temporary files
        self.input_json_path = 'tests/test_generated_input.json'
        # Specify the output file name, not just the directory
        self.output_extsettings_path = os.path.join('tests', 'test_output.ExtSettings')

        # Ensure the output directory exists
        output_dir = os.path.dirname(self.output_extsettings_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        self.test_data = {
            "ProjectFiles": {
                "HeaderPath": ["../../Inc", "../../Another/Path"]
            },
            "Groups": {
                "Doc": ["$PROJ_DIR$/../readme.txt"],
                "Lib": ["../src/main.c", "$../src/main.h"],
                "Drivers/BSP/MyRefBoard": ["C:/MyRefBoard/BSP/board_init.c", "C:/MyRefBoard/BSP/board_init.h"]
            },
            "Others": {
                "Define": ["DEFINE_PREPROCESSOR"],
                "HALModule": ["I2S", "I2C"]
            }
        }

        with open(self.input_json_path, 'w') as f:
            json.dump(self.test_data, f)

    def tearDown(self):
        # Remove the output file
        if os.path.exists(self.output_extsettings_path):
            os.remove(self.output_extsettings_path)
        # Optionally, remove the input file if not needed for other tests
        if os.path.exists(self.input_json_path):
            os.remove(self.input_json_path)

    def test_generate_ext_settings(self):
        manager = ExtSettingsManager(self.input_json_path, self.output_extsettings_path)
        manager.generate_ext_settings(self.test_data)

        # Check if the output file exists
        self.assertTrue(os.path.exists(self.output_extsettings_path))

        # Open and read the output file for content verification
        with open(self.output_extsettings_path, 'r') as f:
            lines = f.read()
            # Assertions updated to reflect actual data structure
            self.assertIn("[ProjectFiles]", lines)
            self.assertIn("HeaderPath=../../Inc;../../Another/Path", lines)
            self.assertIn("[Groups]", lines)
            self.assertIn("[Others]", lines)
            self.assertIn("Define=DEFINE_PREPROCESSOR", lines)


if __name__ == '__main__':
    unittest.main()
