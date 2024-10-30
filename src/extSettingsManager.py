import json
import os
import inquirer


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
                # Toujours ajouter un point-virgule pour Groups et Others
                # Ou si append_semicolon est True (pour ProjectFiles)
                if append_semicolon or section_name in ["Groups", "Others"]:
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

    def read_ext_settings(self):
        """Reads and parses the .extSettings file."""
        result = {}
        current_section = None
        current_config = None

        with open(self.input_json_path, 'r') as file:  # Using input_json_path as input
            for line in file:
                line = line.strip()
                if not line:
                    continue

                if line.startswith('['):
                    # Handle section headers
                    section = line[1:-1]  # Remove brackets
                    if ':' in section:
                        # Handle split configuration case
                        config_name, section_name = section.split(':')
                        if config_name not in result:
                            result[config_name] = {}
                        if section_name not in result[config_name]:
                            result[config_name][section_name] = {}
                        current_section = section_name
                        current_config = result[config_name]
                    else:
                        # Handle direct section case
                        if section not in result:
                            result[section] = {}
                        current_section = section
                        current_config = result
                else:
                    # Handle key-value pairs
                    if '=' in line:
                        key, value = line.split('=', 1)
                        # Remove trailing semicolon and split on semicolons
                        values = [v for v in value.rstrip(';').split(';') if v]
                        if current_config and current_section:
                            current_config[current_section][key] = values

        return result

    def save_json(self, data):
        """Saves data to a JSON file."""
        with open(self.output_extsettings_path, 'w') as file:  # Using output_extsettings_path as output
            json.dump(data, file, indent=2)

    def convert_ext_settings_to_json(self):
        """Converts .extSettings file to JSON format."""
        data = self.read_ext_settings()
        self.save_json(data)

    def load_middleware(self, middleware_name: str, middleware_dir: str = "middlewares") -> dict:
        """Charge la configuration d'un middleware."""
        middleware_path = os.path.join(middleware_dir, f"{middleware_name.lower()}.json")
        try:
            with open(middleware_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception(f"Middleware {middleware_name} not found")

    def prompt_middleware_options(self, middleware_config: dict) -> dict:
        """Interface utilisateur pour sélectionner version et variante."""
        results = {}

        # Sélection de la version
        versions = [v["version"] for v in middleware_config["versions"]]
        version_question = [inquirer.List('version',
                                          message="Select version",
                                          choices=versions)]
        version_answer = inquirer.prompt(version_question)
        if not version_answer:  # Si l'utilisateur annule
            raise Exception("Version selection cancelled")
        results['version'] = version_answer['version']

        # Récupération de la configuration de la version sélectionnée
        selected_version = next(v for v in middleware_config["versions"]
                                if v["version"] == results['version'])

        # Sélection de la variante
        variants = [v["name"] for v in selected_version["variants"]]
        variant_question = [inquirer.List('variant',
                                          message="Select variant",
                                          choices=variants)]
        variant_answer = inquirer.prompt(variant_question)
        if not variant_answer:  # Si l'utilisateur annule
            raise Exception("Variant selection cancelled")
        results['variant'] = variant_answer['variant']

        return results

    def prompt_middleware_variables(self, variant_config: dict) -> dict:
        """Interface utilisateur pour configurer les variables."""
        questions = []
        for var_name, var_config in variant_config.get("variables", {}).items():
            if var_config["type"] == "choice":
                questions.append(inquirer.List(
                    var_name,
                    message=var_config["description"],
                    choices=var_config["choices"],
                    default=var_config["default"]
                ))
            elif var_config["type"] == "number":
                questions.append(inquirer.Text(
                    var_name,
                    message=f"{var_config['description']} ({var_config['min']}-{var_config['max']})",
                    validate=lambda _, x: var_config["min"] <= int(x) <= var_config["max"],
                    default=str(var_config["default"])
                ))
            elif var_config["type"] == "path":
                questions.append(inquirer.Path(
                    var_name,
                    message=var_config["description"],
                    default=var_config["default"],
                    exists=False  # Le chemin n'a pas besoin d'exister car il sera créé par CubeMX
                ))

        answers = inquirer.prompt(questions)
        if not answers:
            raise Exception("Variable configuration cancelled")

        # Normaliser les chemins (convertir les backslashes en slashes)
        for var_name, value in answers.items():
            if variant_config["variables"][var_name]["type"] == "path":
                # Normaliser le chemin et enlever le ./ ou .\ initial si présent
                normalized_path = os.path.normpath(value).replace('\\', '/')
                if normalized_path.startswith('./'):
                    normalized_path = normalized_path[2:]
                answers[var_name] = normalized_path

        return answers

    def apply_middleware(self, middleware_name: str, middleware_dir: str = "middlewares"):
        """Applique un middleware à la configuration actuelle."""
        try:
            # Charger la configuration du middleware
            middleware_config = self.load_middleware(middleware_name, middleware_dir)

            # Obtenir les choix de l'utilisateur
            options = self.prompt_middleware_options(middleware_config)
            if not options:
                raise Exception("No options selected")

            # Récupérer la configuration de la variante sélectionnée
            version = next(v for v in middleware_config["versions"]
                           if v["version"] == options["version"])
            variant = next(v for v in version["variants"]
                           if v["name"] == options["variant"])

            # Obtenir les valeurs des variables
            variables = self.prompt_middleware_variables(variant)
            if not variables:
                raise Exception("No variables configured")

            # Appliquer les variables à la configuration
            config = self._process_middleware_config(variant, variables)

            # Charger la configuration existante ou créer une nouvelle
            existing_config = {"ProjectFiles": {}, "Groups": {}, "Others": {}}

            # Vérifier d'abord le fichier de sortie existant
            if os.path.exists(self.output_extsettings_path):
                try:
                    # Lire la configuration existante depuis le fichier .extSettings
                    existing_config = self.read_ext_settings()
                except Exception as e:
                    print(f"Warning: Could not read existing .extSettings file: {str(e)}")
                    print("Starting with empty configuration.")

            # Fusionner les configurations
            self._merge_configs(existing_config, config)

            # Sauvegarder la configuration
            self.generate_ext_settings(existing_config)

        except Exception as e:
            print(f"Error applying middleware: {str(e)}")
            raise

    def _process_middleware_config(self, variant: dict, variables: dict) -> dict:
        """Traite la configuration du middleware en appliquant les variables."""
        import copy

        config = copy.deepcopy(variant)
        del config["variables"]  # Supprimer la section variables

        # Fonction récursive pour appliquer les variables
        def apply_variables(obj):
            if isinstance(obj, str):
                for var_name, var_value in variables.items():
                    obj = obj.replace(f"{{{var_name}}}", str(var_value))
                return obj
            elif isinstance(obj, list):
                return [apply_variables(item) for item in obj]
            elif isinstance(obj, dict):
                return {k: apply_variables(v) for k, v in obj.items()}
            return obj

        return apply_variables(config)

    def _merge_configs(self, base: dict, other: dict):
        """Fusionne deux configurations."""
        for section in ["ProjectFiles", "Groups", "Others"]:
            if section not in base:
                base[section] = {}
            if section in other:
                for key, values in other[section].items():
                    if key in base[section]:
                        base[section][key].extend(values)
                    else:
                        base[section][key] = values


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
