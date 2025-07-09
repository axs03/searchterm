import sys
from gpt4all import GPT4All
import os
import pkg_resources
from configparser import ConfigParser, NoSectionError, NoOptionError

RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

class Model:
    def __init__(self):
        self.model_path = self.get_model_path()
        self.model_name = self.get_model_name()


    def get_model_path(self):
        """Get the path to the models directory"""
        # current directory
        if os.path.exists("models"):
            return "models"
        
        # user's home directory
        home_models = os.path.expanduser("~/.searchterm/models")
        if os.path.exists(home_models):
            return home_models
        
        # models directory in home
        os.makedirs(home_models, exist_ok=True)
        return home_models


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
        
        # users home directory
        home_config = os.path.expanduser("~/.searchterm/config.ini")
        if os.path.exists(home_config):
            return home_config
        
        return None


    def get_model_name(self):
        # read the config files and get parameters
        try:
            config = ConfigParser()
            config_path = self.get_config_path()
            
            if config_path is None:
                raise FileNotFoundError("Config file not found in any of the expected locations")
            
            config.read(config_path)
            MODEL = config.get("Settings", "MODEL")

            return MODEL
            
        except (FileNotFoundError, NoSectionError, NoOptionError) as e:
            print(f"{RED}Error reading configuration file: {e}")
            print(f"Please ensure the config.ini file exists and is correctly formatted.{RESET}")
            sys.exit(1)


    def download_model(self):
        # start downloading the model
        try:
            model_config = GPT4All.retrieve_model(
                model_name=self.model_name,
                model_path=self.model_path,
                allow_download=True,
                verbose=True
            )
            print(f"{GREEN}Model ready at: {model_config['path']}{RESET}")


        except FileNotFoundError as e:
            print(f"{RED}Error: {e}")
            print(f"Failed to find or download model: {self.model_name}")
            print(f"Please check your internet connection or model name.{RESET}")
            sys.exit(1)
        except Exception as e:
            print(f"{RED}Error loading model: {e}{RESET}")
            sys.exit(1)


    def verify_model(self):
        """Check if the specified model file exists in the given path.
        Returns the model if downloaded, else None"""
        model_file = os.path.join(self.model_path, self.model_name)
        if os.path.exists(model_file):
            model = GPT4All(
                model_name=self.model_name,
                model_path=self.model_path,
                allow_download=False  # already handled the model checking earlier
            )
            return model
        
        return None