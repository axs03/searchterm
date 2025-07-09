#!/bin/bash

clear

echo "=========================================="
echo "       searchterm Installation Script    "
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python 3 is installed
echo -e "${BLUE}Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed. Please install Python 3 first.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}Found Python ${PYTHON_VERSION}${NC}"

# Check if pip is installed
echo -e "${BLUE}Checking pip installation...${NC}"
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}Error: pip3 is not installed. Please install pip3 first.${NC}"
    exit 1
fi
echo -e "${GREEN}pip3 is available${NC}"

# Navigate to the parent directory (where setup.py is located)
cd "$(dirname "$0")/.."

echo -e "${BLUE}Installing searchterm...${NC}"
echo "Current directory: $(pwd)"

# Install the package in development mode
if pip3 install -e .; then
    echo -e "${GREEN}✓ searchterm installed successfully!${NC}"
else
    echo -e "${RED}✗ Installation failed!${NC}"
    exit 1
fi

# Create user config directory
USER_CONFIG_DIR="$HOME/.searchterm"
echo -e "${BLUE}Setting up user configuration...${NC}"

if [ ! -d "$USER_CONFIG_DIR" ]; then
    mkdir -p "$USER_CONFIG_DIR"
    echo -e "${GREEN}✓ Created config directory: $USER_CONFIG_DIR${NC}"
fi

# Copy config file if it doesn't exist
if [ ! -f "$USER_CONFIG_DIR/config.ini" ]; then
    cp config.ini "$USER_CONFIG_DIR/"
    echo -e "${GREEN}✓ Copied default configuration${NC}"
fi

# Create models directory
MODELS_DIR="$USER_CONFIG_DIR/models"
if [ ! -d "$MODELS_DIR" ]; then
    mkdir -p "$MODELS_DIR"
    echo -e "${GREEN}✓ Created models directory: $MODELS_DIR${NC}"
fi

# Copy model file if it exists in the local models directory
if [ -f "models/Phi-3-mini-4k-instruct.Q4_0.gguf" ]; then
    if [ ! -f "$MODELS_DIR/Phi-3-mini-4k-instruct.Q4_0.gguf" ]; then
        echo -e "${BLUE}Copying model file...${NC}"
        cp "models/Phi-3-mini-4k-instruct.Q4_0.gguf" "$MODELS_DIR/"
        echo -e "${GREEN}✓ Model file copied${NC}"
    else
        echo -e "${YELLOW}Model file already exists in user directory${NC}"
    fi
else
    echo -e "${YELLOW}Warning: Model file not found in local models directory${NC}"
    echo -e "${YELLOW}Please place your model file in: $MODELS_DIR${NC}"
fi

echo ""
echo -e "${GREEN}=========================================="
echo -e "           Installation Complete!        "
echo -e "==========================================${NC}"
echo ""
echo -e "${BLUE}Usage:${NC}"
echo "  st \"Your question here\""
echo ""
echo -e "${BLUE}Examples:${NC}"
echo "  st \"What is artificial intelligence?\""
echo "  st \"Explain quantum computing\" --max_tokens 500"
echo ""
echo -e "${BLUE}Configuration:${NC}"
echo "  Config file: $USER_CONFIG_DIR/config.ini"
echo "  Models directory: $MODELS_DIR"
echo ""
echo -e "${BLUE}For help:${NC}"
echo "  st --help"
