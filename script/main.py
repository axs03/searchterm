from gpt4all import GPT4All
import os
import argparse
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

MAX_TOKENS = config.getint("Model Settings", "MAX_TOKENS")
TEMP = config.getfloat("Model Settings", "TEMP")
REPEAT_PENALTY = config.getfloat("Model Settings", "REPEAT_PENALTY")
STREAMING = config.getboolean("Model Settings", "STREAMING")
MODEL = config.get("Model Settings", "MODEL").strip('"')  # Remove quotes from read string
MODEL_PATH = os.path.join(os.getcwd(), "models")

parser = argparse.ArgumentParser(description="A simple script to generate small responses to questions.")
parser.add_argument("prompt", type=str, help="Your prompt for the model")
parser.add_argument("--max_tokens", type=int, default=MAX_TOKENS, help="Maximum tokens for response")
parser.add_argument("--temp", type=float, default=TEMP, help="Temperature for response")
parser.add_argument("--repeat_penalty", type=float, default=REPEAT_PENALTY, help="Repeat penalty for response")
parser.add_argument("--streaming", type=bool, default=STREAMING, help="Streaming for response")
args = parser.parse_args()

model = GPT4All(model_name=MODEL,
                model_path=MODEL_PATH
                )
                
with model.chat_session():
    print(model.generate(prompt = args.prompt, 
                         max_tokens=args.max_tokens, 
                         temp=args.temp, 
                         repeat_penalty=args.repeat_penalty, 
                         streaming=args.streaming))
