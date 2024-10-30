# STM32CubeMX .extSettings Generator - Usage Guide

This tool allows you to generate and manage `.extSettings` files used by STM32CubeMX. It supports both single-core and multi-core configurations, as well as middleware integration.

## Installation

First, install required dependencies:
```bash
pip install -r requirements.txt
```

## Running Tests

To run the test suite:
```bash
python -m unittest tests/test_extSettingsManager.py
```

## Basic Usage

 ### Converting JSON to .extSettings

Convert a JSON configuration file to .extSettings format:
```bash
python src/extSettingsManagerCLI.py --input examples/example.json --output examples/result.extSettings
```

The input JSON file (`examples/example.json`) should contain your project configuration with sections like ProjectFiles, Groups, and Others. For multi-core configurations, use core names as top-level keys (e.g., "CM4", "CM7").

Example JSON structure:
```json
{
  "ProjectFiles": {
    "HeaderPath": ["../../Inc", "../../Another/Path"]
  },
  "Groups": {
    "Doc": ["$PROJ_DIR$/../readme.txt"],
    "Lib": ["../src/main.c", "../src/main.h"]
  },
  "Others": {
    "Define": ["DEFINE_PREPROCESSOR"],
    "HALModule": ["I2S", "I2C"]
  }
}
```

## Adding Middleware

Add a middleware configuration to your .extSettings file:
```bash
python src/extSettingsManagerCLI.py --middleware FreeRTOS --middleware-dir examples/middleware --output examples/result.extSettings
```

The tool will:

1. Read the middleware configuration from examples/middleware/freertos.json
2. Prompt for version selection
3. Prompt for variant selection (e.g., CM4, CM7)
4. Ask for middleware-specific configuration (e.g., heap type, priorities)
5. Generate or update the .extSettings file with the middleware configuration

If the output file already exists, the middleware configuration will be merged with the existing content.

## Multi-Core Configuration

For multi-core devices, structure your input JSON with core-specific configurations:

```json
{
  "CM7": {
    "ProjectFiles": { ... },
    "Groups": { ... },
    "Others": { ... }
  },
  "CM4": {
    "ProjectFiles": { ... },
    "Groups": { ... },
    "Others": { ... }
  }
}
```

Use the same command as for basic conversion:
```bash
python src/extSettingsManagerCLI.py --input examples/dual_core.json --output examples/result.extSettings
```

## File Descriptions
- `examples/example.json`: Example single-core configuration
- `examples/dual_core.json`: Example dual-core configuration
- `examples/middleware/freertos.json`: FreeRTOS middleware configuration template
- `examples/result.extSettings`: Generated .extSettings file

## Common Use Cases
1. New Project Setup: Create a basic `.extSettings` from JSON
2. Add Middleware: Integrate middleware like FreeRTOS, LwIP or MbedTLS into existing configuration
3. Multi-Core Setup: Configure different settings for each core in dual-core STM32 devices

## Notes

- The tool automatically detects if the input JSON contains multi-core configurations.
- Middleware configurations are merged with existing settings if the output file exists.
- All paths in the generated file use forward slashes (/) for compatibility.