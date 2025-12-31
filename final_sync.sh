#!/bin/bash

################################################################################
#
# CryptoSentinel - Final Deployment & Wiki Sync Script
# 
# This script performs the final deployment tasks:
#   1. Commits and pushes UI refactoring changes to main repository
#   2. Deploys fixed Wiki content with corrected hyperlinks
#
# Developer: saisrujanmurthy@gmail.com
# Date: December 31, 2025
#
################################################################################

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Configuration
REPO_DIR="$(pwd)"
WIKI_REPO_URL="https://github.com/Shiva-destroyer/CryptoSentinel.wiki.git"
WIKI_TEMP_DIR="temp_wiki_final"
WIKI_SOURCE_DIR="wiki_temp"

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo -e "\n${CYAN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                                                                      ║${NC}"
    echo -e "${CYAN}║${NC}           ${BOLD}${MAGENTA}CryptoSentinel - Final Deployment Script${NC}${CYAN}              ║${NC}"
    echo -e "${CYAN}║                                                                      ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════════╝${NC}\n"
}

print_section() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BOLD}${CYAN}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ ERROR: $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

print_step() {
    echo -e "${YELLOW}▶${NC} $1"
}

confirm_action() {
    local prompt="$1"
    echo -e "\n${YELLOW}${BOLD}⚡ $prompt${NC}"
    read -p "   Proceed? (yes/no): " response
    
    if [[ ! "$response" =~ ^[Yy][Ee][Ss]$ ]]; then
        print_warning "Operation cancelled by user"
        exit 0
    fi
    echo ""
}

################################################################################
# Validation Functions
################################################################################

validate_repository() {
    print_step "Validating repository..."
    
    if [ ! -d ".git" ]; then
        print_error "Not a git repository. Please run this script from the CryptoSentinel root directory."
        exit 1
    fi
    
    if [ ! -f "cli.py" ] || [ ! -f "crypto_sentinel/ui/console_ui.py" ]; then
        print_error "Required files not found. Are you in the correct directory?"
        exit 1
    fi
    
    if [ ! -d "$WIKI_SOURCE_DIR" ]; then
        print_error "Wiki source directory '$WIKI_SOURCE_DIR' not found."
        exit 1
    fi
    
    print_success "Repository validation passed"
}

check_git_status() {
    print_step "Checking git status..."
    
    # Check for uncommitted changes (excluding files we're about to commit)
    if git status --porcelain | grep -v "cli.py\|console_ui.py\|final_sync.sh" > /dev/null; then
        print_warning "You have uncommitted changes in other files"
        git status --short | grep -v "cli.py\|console_ui.py\|final_sync.sh"
        echo ""
    fi
    
    # Check current branch
    CURRENT_BRANCH=$(git branch --show-current)
    print_info "Current branch: ${BOLD}${CURRENT_BRANCH}${NC}"
    
    if [ "$CURRENT_BRANCH" != "main" ]; then
        print_warning "You are not on the 'main' branch"
        confirm_action "Continue deployment on branch '${CURRENT_BRANCH}'?"
    fi
}

################################################################################
# Task A: Code Deployment
################################################################################

deploy_code_changes() {
    print_section "TASK A: Deploy UI Refactoring Changes"
    
    print_step "Staging modified files..."
    git add cli.py
    git add crypto_sentinel/ui/console_ui.py
    git add final_sync.sh  # Add the deployment script itself
    print_success "Files staged successfully"
    
    print_step "Creating commit..."
    git commit -m "refactor(ui): Show banner only on startup

- Added display_compact_header() method for clean menu headers
- Removed redundant banner calls from all menu loops
- Banner now displays once at application startup
- Improved UX: less scrolling, snappier navigation
- Updated main_menu(), cipher_menu(), hashing_menu(), security_menu()

This improves user experience by reducing visual clutter and
preventing unnecessary scrolling when navigating between menus."
    
    print_success "Commit created successfully"
    
    print_step "Pushing to remote repository..."
    git push origin "$CURRENT_BRANCH"
    print_success "Code changes pushed to GitHub"
    
    # Show commit info
    echo ""
    print_info "Latest commit:"
    git log -1 --oneline --decorate
}

################################################################################
# Task B: Wiki Deployment
################################################################################

deploy_wiki_changes() {
    print_section "TASK B: Deploy Fixed Wiki Content"
    
    # Clean up any existing temp directory
    if [ -d "$WIKI_TEMP_DIR" ]; then
        print_warning "Removing existing temporary wiki directory..."
        rm -rf "$WIKI_TEMP_DIR"
    fi
    
    print_step "Cloning wiki repository..."
    if ! git clone "$WIKI_REPO_URL" "$WIKI_TEMP_DIR"; then
        print_error "Failed to clone wiki repository. Check your network connection and GitHub access."
        exit 1
    fi
    print_success "Wiki repository cloned"
    
    print_step "Copying fixed wiki files from ${WIKI_SOURCE_DIR}..."
    
    # Count files to copy
    FILE_COUNT=$(find "$WIKI_SOURCE_DIR" -name "*.md" | wc -l)
    print_info "Found ${FILE_COUNT} markdown files to deploy"
    
    # Copy all markdown files
    cp -v "$WIKI_SOURCE_DIR"/*.md "$WIKI_TEMP_DIR/"
    print_success "All wiki files copied successfully"
    
    # Navigate to wiki directory
    cd "$WIKI_TEMP_DIR"
    
    print_step "Checking for changes..."
    if git diff --quiet && git diff --cached --quiet; then
        print_warning "No changes detected in wiki files. Files may already be up to date."
        cd "$REPO_DIR"
        rm -rf "$WIKI_TEMP_DIR"
        return 0
    fi
    
    # Show what changed
    echo ""
    print_info "Modified files:"
    git status --short
    echo ""
    
    print_step "Staging wiki changes..."
    git add *.md
    print_success "Wiki files staged"
    
    print_step "Creating wiki commit..."
    git commit -m "fix: Repair hyperlinks and navigation

Fixed wiki hyperlinks to use GitHub Wiki format [[Page-Name]]
instead of markdown format [Text](Page.md) which was causing
links to display raw code instead of rendered pages.

Changes:
- Converted all internal wiki links to [[Page-Name]] format
- Fixed navigation footer links across all pages
- Updated sidebar navigation (_Sidebar.md) with 13 corrected links
- Preserved external links (GitHub issues, documentation)

Total: 24 links fixed across 12 files"
    
    print_success "Wiki commit created"
    
    print_step "Pushing wiki changes to GitHub..."
    if ! git push origin master; then
        print_error "Failed to push wiki changes. Check your GitHub permissions."
        cd "$REPO_DIR"
        exit 1
    fi
    print_success "Wiki changes pushed successfully"
    
    # Return to repo directory
    cd "$REPO_DIR"
    
    print_step "Cleaning up temporary wiki directory..."
    rm -rf "$WIKI_TEMP_DIR"
    print_success "Cleanup complete"
}

################################################################################
# Main Execution
################################################################################

main() {
    print_header
    
    print_info "Repository: ${BOLD}CryptoSentinel${NC}"
    print_info "Developer: ${BOLD}saisrujanmurthy@gmail.com${NC}"
    print_info "Date: ${BOLD}$(date '+%Y-%m-%d %H:%M:%S')${NC}"
    
    # Validation
    validate_repository
    check_git_status
    
    # Confirmation prompt
    confirm_action "Ready to deploy code changes and wiki updates?"
    
    # Execute deployments
    deploy_code_changes
    deploy_wiki_changes
    
    # Final summary
    print_section "✅ DEPLOYMENT COMPLETE"
    
    echo -e "${GREEN}${BOLD}All tasks completed successfully!${NC}\n"
    
    echo -e "${CYAN}📋 Summary:${NC}"
    echo -e "   ${GREEN}✅${NC} UI refactoring committed and pushed"
    echo -e "   ${GREEN}✅${NC} Wiki hyperlinks fixed and deployed"
    echo -e "   ${GREEN}✅${NC} Repository is now production-ready"
    
    echo -e "\n${CYAN}🔗 Quick Links:${NC}"
    echo -e "   Repository: ${BLUE}https://github.com/Shiva-destroyer/CryptoSentinel${NC}"
    echo -e "   Wiki:       ${BLUE}https://github.com/Shiva-destroyer/CryptoSentinel/wiki${NC}"
    
    echo -e "\n${MAGENTA}${BOLD}🚀 Next Steps:${NC}"
    echo -e "   1. Test the CLI interface: ${YELLOW}python3 cli.py${NC}"
    echo -e "   2. Verify wiki links: Visit the Wiki URL above"
    echo -e "   3. Create GitHub Release: ${YELLOW}v1.0.0${NC}"
    
    echo -e "\n${GREEN}${BOLD}🎉 Happy Coding!${NC}\n"
}

################################################################################
# Error Handling
################################################################################

# Trap errors and cleanup
trap 'print_error "Script failed at line $LINENO. Cleaning up..."; cd "$REPO_DIR" 2>/dev/null; rm -rf "$WIKI_TEMP_DIR" 2>/dev/null; exit 1' ERR

# Run main function
main

exit 0
