from src.extSettingsManager import ExtSettingsManager


def main():
    # Hardcoded paths for demonstration purposes
    input_json_path = 'examples/example.json'    # Update with your actual path
    output_extsettings_path = 'examples/.extSettings'        # Update with your actual path

    manager = ExtSettingsManager(input_json_path, output_extsettings_path)
    data = manager.read_input_json()
    manager.generate_ext_settings(data)

    print(f'Generated .extSettings file at {output_extsettings_path}')


if __name__ == "__main__":
    main()
