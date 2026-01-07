#!/bin/bash

# DevEcho - Quick Tweet Poster
# Double-click this file to post a tweet instantly!

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         DevEcho Quick Poster           ║${NC}"
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo -e "${GREEN}✓ Found virtual environment${NC}"
    source venv/bin/activate
else
    echo -e "${YELLOW}⚠ No virtual environment found${NC}"
    echo -e "${YELLOW}  Using system Python...${NC}"
fi

echo ""
echo -e "${BLUE}🐦 Generating and posting tweet...${NC}"
echo ""

# Run the bot
python3 bot.py post-now

# Check exit status
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo -e "${GREEN}✓ Tweet posted successfully!${NC}"
    echo -e "${GREEN}════════════════════════════════════════${NC}"
else
    echo ""
    echo -e "${RED}════════════════════════════════════════${NC}"
    echo -e "${RED}✗ Failed to post tweet${NC}"
    echo -e "${RED}  Check bot.log for details${NC}"
    echo -e "${RED}════════════════════════════════════════${NC}"
fi

echo ""
echo -e "${YELLOW}Press Enter to close...${NC}"
read
