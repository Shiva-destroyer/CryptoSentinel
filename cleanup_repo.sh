#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════
# CryptoSentinel Repository Cleanup Script
# Author: saisrujanmurthy@gmail.com
# Description: Remove temporary setup and deployment files for clean release
# ═══════════════════════════════════════════════════════════════════════════

set -e

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}═══════════════════════════════════════════════════════════════════════════"
echo "  🧹 CryptoSentinel Repository Cleanup"
echo "═══════════════════════════════════════════════════════════════════════════${NC}\n"

# Files to remove
FILES_TO_REMOVE=(
    "PROJECT_MAPPING.txt"
    "PROJECT_STATUS.txt"
    "FINAL_DEPLOYMENT_REPORT.md"
    "DEPLOYMENT_STATUS.md"
    "CLI_IMPLEMENTATION.md"
    "HASHING_SECURITY_SUMMARY.md"
    "INITIALIZATION_COMPLETE.md"
    "QUICK_REFERENCE.md"
    "fix_wiki.sh"
)

echo -e "${CYAN}📋 Files marked for removal:${NC}"
for file in "${FILES_TO_REMOVE[@]}"; do
    if [ -f "$file" ]; then
        echo -e "  ${YELLOW}→ $file${NC}"
    fi
done
echo ""

# Count existing files
FOUND_COUNT=0
for file in "${FILES_TO_REMOVE[@]}"; do
    if [ -f "$file" ]; then
        ((FOUND_COUNT++))
    fi
done

if [ $FOUND_COUNT -eq 0 ]; then
    echo -e "${GREEN}✓ Repository is already clean!${NC}"
    echo -e "${CYAN}ℹ No temporary files found${NC}\n"
    exit 0
fi

echo -e "${YELLOW}⚠ This will permanently delete $FOUND_COUNT files${NC}"
echo -e "${CYAN}ℹ These are temporary setup/deployment files no longer needed${NC}\n"
echo -e "${CYAN}Press CTRL+C within 3 seconds to cancel...${NC}\n"
sleep 3

# Remove files
echo -e "${CYAN}🗑️  Removing temporary files...${NC}\n"

REMOVED_COUNT=0
for file in "${FILES_TO_REMOVE[@]}"; do
    if [ -f "$file" ]; then
        echo -e "  ${CYAN}Removing: $file${NC}"
        rm "$file"
        ((REMOVED_COUNT++))
        echo -e "  ${GREEN}✓ Removed${NC}\n"
    fi
done

echo -e "${GREEN}═══════════════════════════════════════════════════════════════════════════"
echo "  ✅ CLEANUP COMPLETE!"
echo "═══════════════════════════════════════════════════════════════════════════${NC}\n"

echo -e "${CYAN}Summary:${NC}"
echo -e "  • Files removed: $REMOVED_COUNT"
echo -e "  • Repository is now clean and production-ready"
echo ""

# Commit changes
echo -e "${CYAN}📤 Committing cleanup changes...${NC}"
git add -A
git commit -m "chore: Clean up temporary setup and deployment files

Removed temporary files:
$(for file in "${FILES_TO_REMOVE[@]}"; do echo "- $file"; done)

Repository is now production-ready with clean structure."

echo -e "${GREEN}✓ Changes committed${NC}\n"

echo -e "${CYAN}📤 Pushing to remote...${NC}"
git push origin main
echo -e "${GREEN}✓ Pushed to GitHub${NC}\n"

echo -e "${GREEN}🎉 Repository cleanup complete!${NC}"
echo -e "${CYAN}ℹ Repository: https://github.com/Shiva-destroyer/CryptoSentinel${NC}\n"

exit 0
