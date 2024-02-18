import argparse
from extSettingsManager import ExtSettingsManager


CLI_CONFIG = [
    {
        "name": "--json",
        "type": str,
        "help": "Path to the input JSON configuration file."
    },
    {
        "name": "--out",
        "type": str,
        "help": "Output path for the generated .extSettings file."
    }
]


def main():
    parser = argparse.ArgumentParser(description="Generate .extSettings files from JSON configuration.")
    for config in CLI_CONFIG:
        parser.add_argument(config["name"], type=config["type"], help=config["help"])

    args = parser.parse_args()

    if args.json and args.out:
        manager = ExtSettingsManager(args.json, args.out)
        data = manager.read_input_json()

        manager.generate_ext_settings(data)
        print(f".ExtSettings file generated at {args.out}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
