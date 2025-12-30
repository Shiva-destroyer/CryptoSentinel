#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════
# CryptoSentinel Wiki Fix & Cleanup Script
# Author: saisrujanmurthy@gmail.com
# Description: Deploy wiki documentation and clean up wiki_docs/ from main repo
# ═══════════════════════════════════════════════════════════════════════════

set -e

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
NC='\033[0m'

echo -e "${CYAN}═══════════════════════════════════════════════════════════════════════════"
echo "  🔧 CryptoSentinel Wiki Fix & Cleanup"
echo "═══════════════════════════════════════════════════════════════════════════${NC}\n"

WIKI_URL="https://github.com/Shiva-destroyer/CryptoSentinel.wiki.git"
TEMP_DIR="temp_wiki_deploy"

# Step 1: Verify wiki_docs exists
echo -e "${CYAN}📋 Step 1: Verifying wiki_docs/ directory...${NC}"
if [ ! -d "wiki_docs" ]; then
    echo -e "${RED}✗ Error: wiki_docs/ directory not found!${NC}"
    exit 1
fi

WIKI_COUNT=$(ls -1 wiki_docs/*.md 2>/dev/null | wc -l)
echo -e "${GREEN}✓ Found $WIKI_COUNT wiki pages${NC}\n"

# Step 2: Cleanup any existing temp directory
if [ -d "$TEMP_DIR" ]; then
    echo -e "${YELLOW}⚠ Removing existing temp directory...${NC}"
    rm -rf "$TEMP_DIR"
fi

# Step 3: Clone wiki repository
echo -e "${CYAN}📥 Step 2: Cloning wiki repository...${NC}"
if git clone "$WIKI_URL" "$TEMP_DIR" 2>/dev/null; then
    echo -e "${GREEN}✓ Wiki repository cloned successfully${NC}\n"
else
    echo -e "${RED}✗ Failed to clone wiki repository${NC}"
    echo -e "${YELLOW}⚠ Make sure the wiki is initialized on GitHub${NC}"
    exit 1
fi

# Step 4: Copy all markdown files
echo -e "${CYAN}📋 Step 3: Copying wiki documentation files...${NC}"
cp wiki_docs/*.md "$TEMP_DIR/" 2>/dev/null || {
    echo -e "${RED}✗ Failed to copy wiki files${NC}"
    rm -rf "$TEMP_DIR"
    exit 1
}

echo -e "${GREEN}✓ Copied files:${NC}"
for file in "$TEMP_DIR"/*.md; do
    [ -f "$file" ] && echo -e "  ${MAGENTA}→ $(basename "$file")${NC}"
done
echo ""

# Step 5: Commit and push to wiki
echo -e "${CYAN}📤 Step 4: Committing and pushing to wiki...${NC}"
cd "$TEMP_DIR"

git add *.md

if git diff --cached --quiet; then
    echo -e "${YELLOW}⚠ No changes to commit (wiki already up to date)${NC}"
else
    git commit -m "Deploy comprehensive documentation - 8 wiki pages (5900+ lines)

- Home.md: Project overview and quick start
- Caesar-Cipher.md: Frequency analysis & chi-squared
- Vigenere-Cipher.md: IoC & Kasiski examination  
- Substitution-Cipher.md: Hill climbing algorithm
- XOR-Cipher.md: One-time pad & repeating key
- Morse-Code.md: Binary tree encoding/decoding
- Hashing-Tools.md: MD5, SHA-256, checksums
- Security-Tools.md: Password entropy & Base64

Author: saisrujanmurthy@gmail.com"
    
    echo -e "${GREEN}✓ Commit created${NC}\n"
    
    echo -e "${CYAN}🚀 Pushing to GitHub Wiki...${NC}"
    git push origin master || git push origin main
    echo -e "${GREEN}✓ Wiki deployed successfully!${NC}\n"
fi

cd ..

# Step 6: Cleanup temp directory
echo -e "${CYAN}🧹 Step 5: Cleaning up temporary directory...${NC}"
rm -rf "$TEMP_DIR"
echo -e "${GREEN}✓ Temp directory removed${NC}\n"

# Step 7: Remove wiki_docs from main repository
echo -e "${CYAN}🗑️  Step 6: Removing wiki_docs/ from main repository...${NC}"
echo -e "${YELLOW}⚠ This will delete wiki_docs/ locally and remove it from git${NC}"
echo -e "${CYAN}ℹ Wiki pages are now on GitHub Wiki, no need to keep them here${NC}\n"

# Remove from git
git rm -r wiki_docs/
echo -e "${GREEN}✓ Removed wiki_docs/ from git${NC}"

# Commit the removal
git commit -m "chore: Remove wiki_docs/ from main repo

Wiki documentation has been deployed to GitHub Wiki:
https://github.com/Shiva-destroyer/CryptoSentinel/wiki

All 8 wiki pages are now accessible via the Wiki tab.
This keeps the main repository clean and focused on code."

echo -e "${GREEN}✓ Committed removal${NC}\n"

# Push changes
echo -e "${CYAN}📤 Step 7: Pushing changes to main repository...${NC}"
git push origin main
echo -e "${GREEN}✓ Changes pushed${NC}\n"

# Final summary
echo -e "${GREEN}═══════════════════════════════════════════════════════════════════════════"
echo "  ✅ WIKI DEPLOYMENT & CLEANUP COMPLETE!"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""
echo "  📚 Wiki URL: https://github.com/Shiva-destroyer/CryptoSentinel/wiki"
echo ""
echo "  What was done:"
echo "    ✓ Deployed 8 wiki pages to GitHub Wiki"
echo "    ✓ Removed wiki_docs/ from main repository"
echo "    ✓ Cleaned up temporary files"
echo "    ✓ Pushed changes to main branch"
echo ""
echo "  Wiki Pages (5,900+ lines):"
echo "    • Home.md - Project overview"
echo "    • Caesar-Cipher.md - Frequency analysis"
echo "    • Vigenere-Cipher.md - IoC & Kasiski"
echo "    • Substitution-Cipher.md - Hill climbing"
echo "    • XOR-Cipher.md - One-time pad"
echo "    • Morse-Code.md - Binary tree"
echo "    • Hashing-Tools.md - MD5 & SHA-256"
echo "    • Security-Tools.md - Password entropy"
echo ""
echo "  Main repository is now clean and focused on code! 🎯"
echo ""
echo "═══════════════════════════════════════════════════════════════════════════${NC}\n"

exit 0
