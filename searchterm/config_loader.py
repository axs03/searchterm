import os
import configparser
from pathlib import Path
import pkg_resources
import shutil

RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"

class ConfigLoader:
    def __init__(self):
        self.config_dir = Path.home() / ".searchterm"
        self.config_file = self.config_dir / "config.ini"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # check for write permissions
        if not os.access(self.config_dir, os.W_OK):
            raise PermissionError(f"Config directory not writable: {self.config_dir}")
        
        self.configvalues = self.load_config()
    

    def get_default_config(self):
        """Return default configuration values"""
        return {
            "MODEL": "Phi-3-mini-4k-instruct.Q4_0.gguf",
            "MAX_TOKENS": 128,
            "TEMP": 0.3,
            "REPEAT_PENALTY": 1.1,
            "VERSION": "v1.1.0"
        }
    
    
    def copy_package_config(self):
        """Copy the package config to user directory if it doesn't exist"""
        if not self.config_file.exists():
            try:
                package_config = pkg_resources.resource_filename('searchterm', 'config.ini')
                if os.path.exists(package_config):
                    shutil.copy2(package_config, self.config_file)
                    print(f"{GREEN}Copied default config to {self.config_file}{RESET}")
                    return True
            except Exception as e:
                print(f"{YELLOW}Could not copy package config: {e}{RESET}")
        return False
    

    def load_config(self):
        """Load config from INI file, create default if not exists"""
        config = configparser.ConfigParser()
        
        # copy package config first if user config doesn't exist
        self.copy_package_config()
        
        if self.config_file.exists():
            try:
                config.read(self.config_file)
                loaded_config = {}
                if 'Global' in config:
                    loaded_config["VERSION"] = config['Global'].get('VERSION', 'v1.1.0')
                
                if 'Settings' in config:
                    settings_section = config['Settings']
                    loaded_config.update({
                        "MODEL": settings_section.get('MODEL', 'Phi-3-mini-4k-instruct.Q4_0.gguf'),
                        "MAX_TOKENS": settings_section.getint('MAX_TOKENS', 128),
                        "TEMP": settings_section.getfloat('TEMP', 0.3),
                        "REPEAT_PENALTY": settings_section.getfloat('REPEAT_PENALTY', 1.1),
                    })
                
                # Merge with defaults to ensure all keys exist
                defaults = self.get_default_config()
                defaults.update(loaded_config)
                return defaults
                
            except (configparser.Error, ValueError) as e:
                print(f"{YELLOW}Warning: Config file corrupted ({e}), using defaults{RESET}")
                return self.get_default_config()
        else:
            print(f"{YELLOW}No config file found, creating default config{RESET}")
            default_config = self.get_default_config()
            self.save_config(default_config)
            return default_config
    

    def save_config(self, config_dict):
        """Save config to INI file using the correct structure"""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            config = configparser.ConfigParser()
            
            config['Global'] = {
                'VERSION': str(config_dict.get('VERSION', 'v1.1.0'))
            }
            
            config['Settings'] = {
                'MODEL': str(config_dict.get('MODEL', 'Phi-3-mini-4k-instruct.Q4_0.gguf')),
                'MAX_TOKENS': str(config_dict.get('MAX_TOKENS', 128)),
                'TEMP': str(config_dict.get('TEMP', 0.3)),
                'REPEAT_PENALTY': str(config_dict.get('REPEAT_PENALTY', 1.1))
            }
            
            with open(self.config_file, 'w') as f:
                config.write(f)
            
            # read/write for owner only
            os.chmod(self.config_file, 0o600)
            
            self.configvalues = config_dict

            return True
            
        except (IOError, OSError) as e:
            print(f"{RED}Error saving config: {e}{RESET}")
            return False
    
    def get_config_path(self):
        """Return path to config file for user reference"""
        return str(self.config_file)
    
    
    def reload_config(self):
        """Reload configuration from file"""
        self.configvalues = self.load_config()