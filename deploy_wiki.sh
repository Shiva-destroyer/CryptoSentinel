#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════
# CryptoSentinel Wiki Deployment Script
# Author: saisrujanmurthy@gmail.com
# Description: Deploy wiki documentation to GitHub Wiki
# ═══════════════════════════════════════════════════════════════════════════

set -e

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}═══════════════════════════════════════════════════════════════════════════"
echo "  📚 CryptoSentinel Wiki Deployment"
echo "═══════════════════════════════════════════════════════════════════════════${NC}\n"

WIKI_URL="https://github.com/Shiva-destroyer/CryptoSentinel.wiki.git"
TEMP_DIR="temp_wiki"

# Check if wiki_docs exists
if [ ! -d "wiki_docs" ]; then
    echo -e "${RED}✗ Error: wiki_docs/ directory not found!${NC}"
    exit 1
fi

# Count wiki files
WIKI_COUNT=$(ls -1 wiki_docs/*.md 2>/dev/null | wc -l)
echo -e "${CYAN}📝 Found $WIKI_COUNT wiki pages to deploy${NC}\n"

# Cleanup any existing temp directory
if [ -d "$TEMP_DIR" ]; then
    echo -e "${YELLOW}⚠ Removing existing temp directory...${NC}"
    rm -rf "$TEMP_DIR"
fi

# Clone wiki repository
echo -e "${CYAN}📥 Cloning wiki repository...${NC}"
if git clone "$WIKI_URL" "$TEMP_DIR" 2>/dev/null; then
    echo -e "${GREEN}✓ Wiki repository cloned${NC}"
else
    echo -e "${RED}✗ Failed to clone wiki repository${NC}"
    echo -e "${YELLOW}⚠ Make sure you've initialized the wiki on GitHub first!${NC}"
    echo -e "${CYAN}ℹ Steps to initialize:${NC}"
    echo "   1. Visit: https://github.com/Shiva-destroyer/CryptoSentinel/wiki"
    echo "   2. Click 'Create the first page'"
    echo "   3. Save any content"
    echo "   4. Run this script again"
    exit 1
fi

# Copy wiki files
echo -e "\n${CYAN}📋 Copying wiki documentation files...${NC}"
cp wiki_docs/*.md "$TEMP_DIR/" 2>/dev/null || {
    echo -e "${RED}✗ Failed to copy wiki files${NC}"
    rm -rf "$TEMP_DIR"
    exit 1
}

echo -e "${GREEN}✓ Copied files:${NC}"
for file in "$TEMP_DIR"/*.md; do
    [ -f "$file" ] && echo "  → $(basename "$file")"
done

# Commit and push
cd "$TEMP_DIR"

echo -e "\n${CYAN}📤 Committing changes...${NC}"
git add *.md

if git diff --cached --quiet; then
    echo -e "${YELLOW}⚠ No changes to commit (wiki already up to date)${NC}"
else
    git commit -m "Update comprehensive documentation - 8 wiki pages (5900+ lines)"
    echo -e "${GREEN}✓ Commit created${NC}"
    
    echo -e "\n${CYAN}🚀 Pushing to GitHub Wiki...${NC}"
    git push origin master || git push origin main
    echo -e "${GREEN}✓ Wiki deployed successfully!${NC}"
fi

cd ..

# Cleanup
echo -e "\n${CYAN}🧹 Cleaning up...${NC}"
rm -rf "$TEMP_DIR"
echo -e "${GREEN}✓ Cleanup complete${NC}"

echo -e "\n${GREEN}═══════════════════════════════════════════════════════════════════════════"
echo "  ✅ WIKI DEPLOYMENT COMPLETE!"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""
echo "  📚 Visit your wiki: https://github.com/Shiva-destroyer/CryptoSentinel/wiki"
echo ""
echo "  Wiki Pages Deployed:"
echo "    • Home.md (Landing page)"
echo "    • Caesar-Cipher.md (Frequency analysis)"
echo "    • Vigenere-Cipher.md (IoC & Kasiski)"
echo "    • Substitution-Cipher.md (Hill climbing)"
echo "    • XOR-Cipher.md (One-time pad)"
echo "    • Morse-Code.md (Binary tree)"
echo "    • Hashing-Tools.md (MD5 & SHA-256)"
echo "    • Security-Tools.md (Password & Base64)"
echo ""
echo "═══════════════════════════════════════════════════════════════════════════${NC}\n"

exit 0
