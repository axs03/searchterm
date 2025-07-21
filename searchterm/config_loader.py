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

    
    def get_default_config(self):
        """Return default configuration values"""
        return {
            "VERSION": "v1.1.0",
            "MODEL": "Phi-3-mini-4k-instruct.Q4_0.gguf",
            "MAX_TOKENS": 128,
            "TEMP": 0.3,
            "REPEAT_PENALTY": 1.1,
        }
    

    def save_config(self, modified_config):
        """Save the modified configuration to the config file"""
        try:
            config = ConfigParser()
            
            config.add_section('Global')
            config.add_section('Settings')
            
            config.set('Global', 'VERSION', str(modified_config['VERSION']))
            config.set('Settings', 'MODEL', str(modified_config['MODEL']))
            config.set('Settings', 'MAX_TOKENS', str(modified_config['MAX_TOKENS']))
            config.set('Settings', 'TEMP', str(modified_config['TEMP']))
            config.set('Settings', 'REPEAT_PENALTY', str(modified_config['REPEAT_PENALTY']))

            home_config = os.path.expanduser("~/.searchterm/config.ini") # fix for dynamic path?
            os.makedirs(os.path.dirname(home_config), exist_ok=True)
            
            with open(home_config, 'w') as config_file:
                config.write(config_file)
            
            # update current config path and values
            self.config_file_path = home_config
            self.configvalues = modified_config.copy()
            
            return True
            
        except Exception as e:
            print(f"{RED}Error saving config: {e}{RESET}")
            return False