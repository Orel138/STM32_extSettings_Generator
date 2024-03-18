import json


class ExtSettingsManager:
    def __init__(self, input_json_path, output_extsettings_path):
        self.input_json_path = input_json_path
        self.output_extsettings_path = output_extsettings_path

    def read_input_json(self):
        """Reads JSON data from the specified file path."""
        with open(self.input_json_path, 'r') as file:
            return json.load(file)

    def load_additional_config(self, file_path):
        """Loads additional configurations from a JSON file."""
        return self.read_input_json(file_path)

    def generate_section(self, file, section_name, data, append_semicolon=False):
        """Generates a section in the output file for each key-value pair in the data."""
        keys = list(data.keys())
        for i, key in enumerate(keys):
            value = data[key]
            if isinstance(value, list):
                value_str = ';'.join(value)
                if append_semicolon or (section_name == "Groups" and i < len(keys) - 1):
                    value_str += ';'
                file.write(f"{key}={value_str}\n")

    def is_configuration_split(self, data):
        """Determines if the configuration data is split into sub-configurations or direct sections."""
        for key in data.keys():
            if key in ["ProjectFiles", "Groups", "Others"]:
                return False
        return True

    def generate_ext_settings(self, data):
        """Generates the external settings file based on the provided data."""
        with open(self.output_extsettings_path, 'w') as file:
            if self.is_configuration_split(data):
                for config_name, config_data in data.items():
                    for section_name, section_data in config_data.items():
                        prefixed_section_name = f"[{config_name}:{section_name}]\n"
                        file.write(prefixed_section_name)
                        # Append semicolon logic here if needed, based on section
                        self.generate_section(file, section_name, section_data)
            else:
                for i, (section_name, section_data) in enumerate(data.items()):
                    section_header = f"[{section_name}]\n"
                    file.write(section_header)
                    # Decide on appending semicolon based on section type and potentially item position
                    append_semicolon = section_name == "ProjectFiles"
                    self.generate_section(file, section_name, section_data, append_semicolon=append_semicolon)

    def insert_into_section(self, main_config, additional_config, section, section_name=None):
        """Generic function to insert configurations into a specified section."""
        target = main_config if section_name is None else main_config.get(section_name, {})
        for key, value in additional_config.items():
            if key in target.get(section, {}):
                target[section][key].extend(value)
            else:
                if section not in target:
                    target[section] = {}
                target[section][key] = value
        if section_name is not None and section_name not in main_config:
            main_config[section_name] = target


# Usage example
if __name__ == "__main__":
    input_json_path = 'input-test.json'
    output_extsettings_path = '.extSettings'

    manager = ExtSettingsManager(input_json_path, output_extsettings_path)
    data = manager.read_input_json()

    # Optionally load additional data and insert into specific sections
    # additional_config = manager.load_additional_config('input-test2.json')
    # manager.insert_into_section(data, additional_config, 'ProjectFiles', 'Cortex_M4')

    manager.generate_ext_settings(data)
