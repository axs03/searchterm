# Searchterm - Simple Command-Line AI Question Answering

A simple command-line interface for interacting with AI models using GPT4All.

## Installation

### Automatic Installation

Run the installation script:

```bash
cd installer
chmod +x install_searchterm.sh
./install_searchterm.sh
```

### Manual Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Install the package:

```bash
pip3 install -e .
```

## Usage

Once installed, you can use the `searchterm` command from anywhere in your terminal:

```bash
searchterm "Your question here"
```

### Examples

```bash
# Basic usage
searchterm "What is artificial intelligence?"

# With custom parameters
searchterm "Why is my floor burning" --max_tokens 500 --temp 0.7

# Enable streaming
searchterm "Tell me a story about jelly beans" --streaming

# Use custom config file
searchterm "Hello" --config /path/to/custom/config.ini
```

### Command-line Options

- `prompt`: Your question or prompt (required)
- `--max_tokens`: Maximum tokens for response (default from config)
- `--temp`: Temperature for response (default from config)
- `--repeat_penalty`: Repeat penalty for response (default from config)
- `--streaming`: Enable streaming output
- `--config`: Path to custom configuration file
- `--version`: Show version information
- `--help`: Show help message

## Configuration

The application uses a configuration file located at `~/.searchterm/config.ini`. You can modify this file to change default settings:

```ini
[Model Settings]
MODEL = "Phi-3-mini-4k-instruct.Q4_0.gguf"
MAX_TOKENS = 256
TEMP = 0.5
REPEAT_PENALTY = 1.1
STREAMING = False
```

## Model Files

Place your GGUF model files in the `~/.searchterm/models/` directory. The application will look for the model specified in your configuration file.

## Requirements

- Python 3.7 or higher
- GPT4All Python library
- A compatible GGUF model file

## Troubleshooting

### Model Not Found
If you get a "Model file not found" error:
1. Check that your model file is in `~/.searchterm/models/`
2. Verify the model name in `~/.searchterm/config.ini` matches your file
3. Ensure the model file is a valid GGUF format

### Installation Issues
If installation fails:
1. Make sure you have Python 3.7+ installed
2. Ensure pip3 is available
3. Try installing dependencies manually: `pip3 install gpt4all`

## Uninstall

To uninstall the application:

```bash
pip3 uninstall searchterm
rm -rf ~/.searchterm  # optional: remove config and models
```
