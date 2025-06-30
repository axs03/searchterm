#!/bin/bash

clear

echo "=========================================="
echo "      Searchterm Uninstallation Script   "
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Uninstalling searchterm...${NC}"

# Uninstall the package
if pip3 uninstall searchterm -y; then
    echo -e "${GREEN}✓ Searchterm package uninstalled${NC}"
else
    echo -e "${RED}✗ Failed to uninstall package${NC}"
fi

# Ask user if they want to remove config and models
echo ""
echo -e "${YELLOW}Do you want to remove configuration and model files?${NC}"
echo -e "${YELLOW}This will delete ~/.searchterm directory${NC}"
read -p "Remove config and models? (y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -d "$HOME/.searchterm" ]; then
        rm -rf "$HOME/.searchterm"
        echo -e "${GREEN}✓ Configuration and models removed${NC}"
    else
        echo -e "${YELLOW}No configuration directory found${NC}"
    fi
else
    echo -e "${BLUE}Configuration and models preserved at ~/.searchterm${NC}"
fi

echo ""
echo -e "${GREEN}Uninstallation complete!${NC}"
