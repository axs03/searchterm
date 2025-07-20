#!/usr/bin/env python3
"""
Command-line interface for searchterm AI chat application
"""

import argparse
import sys
from .model import Model
from .config_loader import (
    ConfigLoader,
    RED, YELLOW, GREEN, RESET
)


def main():
    config_loader = ConfigLoader()

    # parse the arguments passed
    parser = argparse.ArgumentParser(
        description="A simple command-line AI chat application.",
        prog="searchterm"
    )
    parser.add_argument("prompt",
                        type=str,
                        help="Your prompt for the model")
    parser.add_argument("--max-tokens", 
                        type=int, 
                        default=config_loader.configvalues["MAX_TOKENS"], 
                        help=f"Maximum tokens for response (default: {config_loader.configvalues['MAX_TOKENS']})")
    parser.add_argument("--temp", 
                        type=float, 
                        default=config_loader.configvalues["TEMP"], 
                        help=f"Temperature for response (default: {config_loader.configvalues['TEMP']})")
    parser.add_argument("--repeat_penalty", 
                        type=float, 
                        default=config_loader.configvalues["REPEAT_PENALTY"], 
                        help=f"Repeat penalty for response (default: {config_loader.configvalues['REPEAT_PENALTY']})")
    parser.add_argument("--version", 
                        action="version", 
                        version="")
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
