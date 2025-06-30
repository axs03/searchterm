#!/usr/bin/env python3
"""
Command-line interface for SearchTerm AI chat application
"""

from gpt4all import GPT4All
import os
import argparse
import configparser
import sys
import pkg_resources


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
    
    # Create default config in home directory
    home_dir = os.path.expanduser("~/.searchterm")
    os.makedirs(home_dir, exist_ok=True)
    default_config = os.path.join(home_dir, "config.ini")
    
    # Create default config
    config = configparser.ConfigParser()
    config['Model Settings'] = {
        'MODEL': 'Phi-3-mini-4k-instruct.Q4_0.gguf',
        'MAX_TOKENS': '256',
        'TEMP': '0.5',
        'REPEAT_PENALTY': '1.1',
        'STREAMING': 'False'
    }
    
    with open(default_config, 'w') as f:
        config.write(f)
    
    return default_config


def get_model_path():
    """Get the path to the models directory"""
    # Try current directory first
    if os.path.exists("models"):
        return "models"
    
    # Try user's home directory
    home_models = os.path.expanduser("~/.searchterm/models")
    if os.path.exists(home_models):
        return home_models
    
    # Create models directory in home
    os.makedirs(home_models, exist_ok=True)
    return home_models


def main():
    """Main entry point for the searchterm command"""
    config = configparser.ConfigParser()
    config_path = get_config_path()
    config.read(config_path)

    # Get configuration values
    try:
        MAX_TOKENS = config.getint("Model Settings", "MAX_TOKENS")
        TEMP = config.getfloat("Model Settings", "TEMP")
        REPEAT_PENALTY = config.getfloat("Model Settings", "REPEAT_PENALTY")
        STREAMING = config.getboolean("Model Settings", "STREAMING")
        MODEL = config.get("Model Settings", "MODEL").strip('"')  # Remove quotes from read string
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(f"Error reading config file {config_path}: {e}")
        print("Please check your configuration file.")
        sys.exit(1)

    MODEL_PATH = get_model_path()

    # Check if model file exists
    model_file = os.path.join(MODEL_PATH, MODEL)
    if not os.path.exists(model_file):
        print(f"Error: Model file not found at {model_file}")
        print(f"Please place your model file in the {MODEL_PATH} directory.")
        print(f"Expected model: {MODEL}")
        sys.exit(1)

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
    parser.add_argument("--streaming", 
                        action="store_true", 
                        default=STREAMING, 
                        help="Enable streaming for response")
    parser.add_argument("--config", 
                        type=str, 
                        help="Path to custom config file")
    parser.add_argument("--version", 
                        action="version", 
                        version="searchterm 1.0.0")

    args = parser.parse_args()

    # Use custom config if provided
    if args.config:
        if os.path.exists(args.config):
            config.read(args.config)
        else:
            print(f"Error: Config file {args.config} not found.")
            sys.exit(1)

    try:
        print("Loading model...")
        model = GPT4All(model_name=MODEL, model_path=MODEL_PATH)
        
        print("Generating response...")
        with model.chat_session():
            response = model.generate(
                prompt=args.prompt, 
                max_tokens=args.max_tokens, 
                temp=args.temp, 
                repeat_penalty=args.repeat_penalty, 
                streaming=args.streaming
            )
            print(response)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
