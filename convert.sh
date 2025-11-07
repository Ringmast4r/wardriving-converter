#!/bin/bash
################################################################################
#   UNIVERSAL WARDRIVING CONVERTER - LINUX/MAC VERSION
################################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT="$SCRIPT_DIR/conversion_vault"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create conversion vault
mkdir -p "$VAULT"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 not found!${NC}"
    echo "Please install Python 3:"
    echo "  Ubuntu/Debian: sudo apt install python3"
    echo "  macOS: brew install python3"
    exit 1
fi

# No arguments? Show help
if [ $# -eq 0 ]; then
    clear
    echo ""
    echo "======================================================================"
    echo "  UNIVERSAL WARDRIVING CONVERTER"
    echo "======================================================================"
    echo ""
    echo "USAGE:"
    echo "  ./convert.sh <file_or_folder> [options]"
    echo ""
    echo "EXAMPLES:"
    echo "  ./convert.sh wigle_data.csv"
    echo "  ./convert.sh wardriving_folder/ --merge"
    echo "  ./convert.sh data/ --recursive --merge"
    echo ""
    echo "OPTIONS:"
    echo "  --merge       Combine all files into one CSV"
    echo "  --recursive   Include subfolders"
    echo ""
    echo "All outputs saved to: $VAULT"
    echo ""
    exit 0
fi

# Get input
INPUT="$1"

# Check if input exists
if [ ! -e "$INPUT" ]; then
    echo -e "${RED}ERROR: Not found: $INPUT${NC}"
    exit 1
fi

# Create timestamped output folder
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FOLDER="$VAULT/$TIMESTAMP"
mkdir -p "$OUTPUT_FOLDER"

echo ""
echo -e "${BLUE}======================================================================"
echo "  UNIVERSAL WARDRIVING CONVERTER"
echo -e "======================================================================${NC}"
echo ""

# Detect if it's a folder or file
if [ -d "$INPUT" ]; then
    echo -e "${GREEN}Detected: FOLDER${NC}"
    echo ""
    echo "What do you want to do?"
    echo ""
    echo "  1. Convert each file separately"
    echo "  2. MERGE all into ONE master CSV  [RECOMMENDED]"
    echo "  3. Recursive + Merge (includes subfolders)"
    echo ""
    read -p "Enter choice (1-3): " choice
    echo ""

    case $choice in
        1)
            python3 "$SCRIPT_DIR/universal_wardrive_converter.py" --folder "$INPUT"
            mv "$INPUT/converted"/* "$OUTPUT_FOLDER/" 2>/dev/null
            rmdir "$INPUT/converted" 2>/dev/null
            ;;
        2)
            python3 "$SCRIPT_DIR/universal_wardrive_converter.py" --folder "$INPUT" --merge
            mv "$INPUT/converted/merged_all.csv" "$OUTPUT_FOLDER/MERGED_ALL.csv" 2>/dev/null
            rmdir "$INPUT/converted" 2>/dev/null
            ;;
        3)
            python3 "$SCRIPT_DIR/universal_wardrive_converter.py" --folder "$INPUT" --recursive --merge
            mv "$INPUT/converted/merged_all.csv" "$OUTPUT_FOLDER/MERGED_ALL.csv" 2>/dev/null
            rmdir "$INPUT/converted" 2>/dev/null
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            exit 1
            ;;
    esac

elif [ -f "$INPUT" ]; then
    echo -e "${GREEN}Detected: FILE${NC}"
    echo ""
    FILENAME=$(basename "$INPUT" | sed 's/\.[^.]*$//')
    python3 "$SCRIPT_DIR/universal_wardrive_converter.py" "$INPUT" "$OUTPUT_FOLDER/${FILENAME}_converted.csv"
else
    echo -e "${RED}ERROR: Unknown input type${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}======================================================================"
echo "  SUCCESS!"
echo -e "======================================================================${NC}"
echo ""
echo "✓ Output saved to: conversion_vault/$TIMESTAMP/"
echo ""

# Open folder (platform specific)
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "$OUTPUT_FOLDER"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v xdg-open &> /dev/null; then
        xdg-open "$OUTPUT_FOLDER" 2>/dev/null
    elif command -v nautilus &> /dev/null; then
        nautilus "$OUTPUT_FOLDER" 2>/dev/null
    fi
fi

echo "Done!"
