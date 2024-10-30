import argparse
import os
from extSettingsManager import ExtSettingsManager


CLI_CONFIG = [
    {
        "name": "--input",
        "type": str,
        "help": "Path to the input file (JSON or .extSettings)",
        "required": False
    },
    {
        "name": "--output",
        "type": str,
        "help": "Path to the output file",
        "required": False
    },
    {
        "name": "--middleware",
        "type": str,
        "help": "Name of middleware to add (e.g., FreeRTOS, LwIP)",
        "required": False
    },
    {
        "name": "--middleware-dir",
        "type": str,
        "help": "Directory containing middleware configurations",
        "default": "middlewares"
    }
]


def get_file_extension(file_path):
    """Get the file extension in lowercase."""
    return os.path.splitext(file_path)[1].lower()


def main():
    parser = argparse.ArgumentParser(description="Convert between .extSettings and JSON formats.")
    for config in CLI_CONFIG:
        parser.add_argument(config["name"],
                            type=config["type"],
                            help=config["help"],
                            required=config.get("required", False),
                            default=config.get("default")
                            )

    args = parser.parse_args()

    if args.middleware:
        # Mode ajout de middleware
        if not args.output:
            parser.error("--output is required when using --middleware")
        manager = ExtSettingsManager(args.output, args.output)
        manager.apply_middleware(args.middleware, args.middleware_dir)
        print(f"Middleware {args.middleware} added to {args.output}")
    elif args.input and args.output:
        # Mode conversion normal
        if args.input and args.output:
            input_ext = get_file_extension(args.input)
            manager = ExtSettingsManager(args.input, args.output)

            if input_ext == '.json':
                data = manager.read_input_json()
                manager.generate_ext_settings(data)
                print(f".extSettings file generated at {args.output}")
            elif input_ext == '.extsettings':
                manager.convert_ext_settings_to_json()
                print(f"JSON file generated at {args.output}")
            else:
                print(f"Error: Input file must be either .json or .extSettings, got: {input_ext}")
                return
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
