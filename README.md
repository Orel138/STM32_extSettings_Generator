# STM32_extSettings_Generator

## Overview
The STM32_extSettings_Generator is a Python tool designed to simplify the development process for STM32 microcontroller projects by converting human-readable JSON files into .extSettings files for use with STM32CubeMX project generation. The .extSettings file facilitates specifying additional project settings such as include directories, file groups, and preprocessor defines, which are crucial for customizing the project setup but can be cumbersome to edit manually.

## Features
- Converts JSON to .extSettings format for easy project configurations.
- Supports custom grouping of files and directories for better project organization.
- Allows specifying preprocessor defines and HAL modules directly through a JSON file.

## Installation

### Clone the Repository
```bash
https://github.com/Orel138/STM32_extSettings_Generator.git
```

## Usage
### Create Your JSON Configuration File
Define your project settings in a JSON file. See `examples/example.json` for structure and syntax.

### Run the Generator
```bash
python ./extSettingsGenerator.py
```

or with a Command-Line Interface (CLI) :
```bash
python src/extSettingsManagerCLI.py --json examples/example.json --out examples/.extSettings
```

## Contributing
Contributions are welcome! Here's how you can help:
- **Report Bugs**: Open an issue describing the bug and how to reproduce it.
- **Suggest Enhancements**: Share your ideas for making the tool better by opening an issue.
- **Pull Requests**: Contribute directly to the code by forking the repository, making your changes, and submitting a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
This tool was created to facilitate STM32 project development using STM32CubeMX. It is not officially associated with STMicroelectronics or the STM32CubeMX tool.
