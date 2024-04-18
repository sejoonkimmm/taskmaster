import yaml
import os

class ConfigError(Exception):
    """ Custom exception for handling configuration errors. """
    pass


class Config:
    """ A class to manage the application configuration file. """
    
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        """ Load the YAML configuration file. """
        if not os.path.exists(self.config_file):
            raise ConfigError(f"Config file does not exist: {self.config_file}")
        
        try:
            with open(self.config_file, 'r') as file:
                config = yaml.safe_load(file)
                self.validate_config(config)
                return config
        except yaml.YAMLError as exc:
            raise ConfigError(f"Error parsing YAML config: {exc}")
        except OSError as exc:
            raise ConfigError(f"Error reading config file: {exc}")

    def validate_config(self, config):
        """ Validate the configuration content structure. """
        if 'programs' not in config or not isinstance(config['programs'], dict):
            raise ConfigError("The 'programs' section is missing or invalid in the configuration file.")
        
        for program_name, settings in config['programs'].items():
            if 'cmd' not in settings:
                raise ConfigError(f"The 'cmd' setting is missing for program '{program_name}'.")

    def reload_config(self):
        """ Reload the configuration from the YAML file. """
        self.config = self.load_config()

    def get_program(self):
        """ Retrieve the 'program' section from the config file. """
        return self.config.get('programs', {})


# You might include other helpful methods or validation logic here.
