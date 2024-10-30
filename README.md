# STM32_extSettings_Generator

## Overview
The STM32_extSettings_Generator is a Python tool designed to simplify the development process for STM32 microcontroller projects by converting human-readable JSON files into .extSettings files for use with STM32CubeMX project generation. The .extSettings file facilitates specifying additional project settings such as include directories, file groups, and preprocessor defines, which are crucial for customizing the project setup but can be cumbersome to edit manually.

## Features
- Converts JSON to .extSettings format for easy project configurations.
- Supports custom grouping of files and directories for better project organization.
- Allows specifying preprocessor defines and HAL modules directly through a JSON file.
- Handles multi-core configurations (e.g., Cortex-M4/M7 dual-core projects)
- Supports middleware integration with version control and variants (FreeRTOS, LwIP, MbedTLS, etc.)
- Provides an interactive CLI for middleware configuration

## Installation

Clone the Repository
```bash
https://github.com/Orel138/STM32_extSettings_Generator.git
```

Install required dependencies
```bash
pip install -r requirements.txt
```

## Usage

For detailed usage instructions and examples, please refer to our [Usage Guide](./docs/Usage.md).

### Create Your JSON Configuration File
Define your project settings in a JSON file. See `examples/example.json` for structure and syntax.

### Run the Generator
```bash
python ./extSettingsGenerator.py
```

or with a Command-Line Interface (CLI) :
```bash
python src/extSettingsManagerCLI.py --input examples/example.json --output examples/.extSettings
```

### Adding middleware to your configuration

```bash
python src/extSettingsManagerCLI.py --middleware FreeRTOS --middleware-dir examples/middleware --output examples/.extSettings
```

For more examples, including multi-core configurations and middleware integration, see the [Usage Guide](./docs/Usage.md).

## Project Structure

- `examples/`: Contains example JSON configurations and middleware templates
- `src/`: Source code for the generator
- `tests/`: Unit tests
- `docs/`: Documentation including detailed usage instructions
- `requirements.txt`: Python dependencies

## Contributing
Contributions are welcome! Here's how you can help:
- **Report Bugs**: Open an issue describing the bug and how to reproduce it.
- **Suggest Enhancements**: Share your ideas for making the tool better by opening an issue.
- **Pull Requests**: Contribute directly to the code by forking the repository, making your changes, and submitting a pull request.
- **Documentation**: Help improve our documentation or add more examples

## License
_STM32_FreeRTOS-Kernel_ is released under the [MIT license](/LICENSE) © [Orel138](https://github.com/Orel138).

## Acknowledgments
This tool was created to facilitate STM32 project development using STM32CubeMX. It is not officially associated with STMicroelectronics or the STM32CubeMX tool.

> [!TIP]
> I trust you'll find this project enjoyable. Should you appreciate the project, bestowing a small ⭐ on it is a meaningful gesture, signifying: **My efforts are recognized.** Your support would be greatly valued. _Many thanks!_