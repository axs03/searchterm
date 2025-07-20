from configparser import ConfigParser, NoSectionError, NoOptionError
import pkg_resources
import os
import sys

# colors for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"


class ConfigLoader:
    def __init__(self):
        self.configparser = ConfigParser()
        self.config_path = self.get_config_path()
        self.configvalues = self.get_config_values()

    def get_config_path(self):
        """Get the path to the config file, checking multiple locations"""
        # current directory first
        if os.path.exists("config.ini"):
            return "config.ini"
        
        # package data
        try:
            return pkg_resources.resource_filename('searchterm', 'config.ini')
        except:
            pass
        
        # user's home directory
        home_config = os.path.expanduser("~/.searchterm/config.ini")
        if os.path.exists(home_config):
            return home_config
        
        return None
    
    def get_config_values(self):
        config = self.configparser
        config_path = self.get_config_path()
        config.read(config_path) # type: ignore

        # get the configuration values
        try:
            return {
                "VERSION": config.get("Global", "VERSION"),
                "MODEL": config.get("Settings", "MODEL"),
                "MAX_TOKENS": config.getint("Settings", "MAX_TOKENS"),
                "TEMP": config.getfloat("Settings", "TEMP"),
                "REPEAT_PENALTY": config.getfloat("Settings", "REPEAT_PENALTY")
            }

        except (NoSectionError, NoOptionError) as e:
            print(f"Error reading config file {config_path}: {e}")
            print("Please check your configuration file.")
            sys.exit(1)