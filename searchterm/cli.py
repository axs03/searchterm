#!/usr/bin/env python3
"""
Command-line interface for SearchTerm AI chat application
"""

import os
import argparse
import configparser
import sys
import pkg_resources
from .model import Model

# colors for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def get_config_path():
    """Get the path to the config file, checking multiple locations"""
    # Try current directory first
    if os.path.exists("config.ini"):
        return "config.ini"
    
    # Try package data
    try:
        return pkg_resources.resource_filename('searchterm', 'config.ini')
    except:
        pass
    
    # Try user's home directory
    home_config = os.path.expanduser("~/.searchterm/config.ini")
    if os.path.exists(home_config):
        return home_config
    

def get_config_values():
    config = configparser.ConfigParser()
    config_path = get_config_path()
    config.read(config_path) # type: ignore

    # get the configuration values
    try:
        MAX_TOKENS = config.getint("Settings", "MAX_TOKENS")
        TEMP = config.getfloat("Settings", "TEMP")
        REPEAT_PENALTY = config.getfloat("Settings", "REPEAT_PENALTY")

        return MAX_TOKENS, TEMP, REPEAT_PENALTY
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(f"Error reading config file {config_path}: {e}")
        print("Please check your configuration file.")
        sys.exit(1)


def main():
    MAX_TOKENS, TEMP, REPEAT_PENALTY = get_config_values()

    # parse the arguments passed
    parser = argparse.ArgumentParser(
        description="A simple command-line AI chat application.",
        prog="searchterm"
    )
    parser.add_argument("prompt", 
                        type=str, 
                        help="Your prompt for the model")
    parser.add_argument("--max_tokens", 
                        type=int, 
                        default=MAX_TOKENS, 
                        help=f"Maximum tokens for response (default: {MAX_TOKENS})")
    parser.add_argument("--temp", 
                        type=float, 
                        default=TEMP, 
                        help=f"Temperature for response (default: {TEMP})")
    parser.add_argument("--repeat_penalty", 
                        type=float, 
                        default=REPEAT_PENALTY, 
                        help=f"Repeat penalty for response (default: {REPEAT_PENALTY})")
    parser.add_argument("--version", 
                        action="version", 
                        version="searchterm v1.1.0-alpha")
    args = parser.parse_args()

    # create the model object instance
    model = Model()
    curr_model = model.verify_model()
    if not curr_model:
        print(f"{YELLOW}Model verification failed. Not found in directory. Would you like to download {model.model_name}? (y/n) : {RESET}")
        choice = input().strip().lower()
        
        if choice == 'y':
            model.download_model()
            # verify model again after download
            curr_model = model.verify_model()
            if not curr_model:
                print(f"{RED}Model download failed or model still not found. Exiting...{RESET}")
                sys.exit(1)
        else:
            print(f"{RED}Model not found and download skipped. Exiting...{RESET}")
            sys.exit(1)


    # infer the model and give an answer
    try:
        with curr_model.chat_session():
            response = curr_model.generate(
                prompt=args.prompt, 
                max_tokens=args.max_tokens, 
                temp=args.temp, 
                repeat_penalty=args.repeat_penalty
            )
            print(response)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
