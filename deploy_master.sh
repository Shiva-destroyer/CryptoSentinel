#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════
# CryptoSentinel Master Deployment Script
# Author: saisrujanmurthy@gmail.com
# Version: 1.0
# Description: Deploys both code repository and wiki documentation to GitHub
# ═══════════════════════════════════════════════════════════════════════════

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Repository configuration
REPO_URL="https://github.com/Shiva-destroyer/CryptoSentinel.git"
WIKI_URL="https://github.com/Shiva-destroyer/CryptoSentinel.wiki.git"
TEMP_WIKI_DIR="temp_wiki"

# Print banner
print_banner() {
    echo -e "${CYAN}${BOLD}"
    echo "═══════════════════════════════════════════════════════════════════════════"
    echo "   ____                  _        ____             _   _            _ "
    echo "  / ___|_ __ _   _ _ __ | |_ ___ / ___|  ___ _ __ | |_(_)_ __   ___| |"
    echo " | |   | '__| | | | '_ \| __/ _ \\\\___ \ / _ \ '_ \| __| | '_ \ / _ \ |"
    echo " | |___| |  | |_| | |_) | || (_) |___) |  __/ | | | |_| | | | |  __/ |"
    echo "  \____|_|   \__, | .__/ \__\___/|____/ \___|_| |_|\__|_|_| |_|\___|_|"
    echo "             |___/|_|                                                  "
    echo ""
    echo "                    MASTER DEPLOYMENT SCRIPT v1.0"
    echo "═══════════════════════════════════════════════════════════════════════════"
    echo -e "${NC}"
}

# Print step header
print_step() {
    echo -e "\n${MAGENTA}${BOLD}▶ $1${NC}"
    echo -e "${BLUE}────────────────────────────────────────────────────────────────${NC}"
}

# Print success message
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Print warning message
print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Print error message
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Print info message
print_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

# ═══════════════════════════════════════════════════════════════════════════
# PART A: DEPLOY CODE REPOSITORY
# ═══════════════════════════════════════════════════════════════════════════

deploy_code() {
    print_step "PART A: DEPLOYING CODE REPOSITORY"
    
    # Step 1: Initialize git repository
    print_info "Initializing Git repository..."
    if [ -d ".git" ]; then
        print_warning "Git repository already exists. Removing..."
        rm -rf .git
    fi
    git init
    print_success "Git repository initialized"
    
    # Step 2: Configure git user (if not set globally)
    if [ -z "$(git config user.name)" ]; then
        print_info "Configuring Git user..."
        git config user.name "Shiva-destroyer"
        git config user.email "saisrujanmurthy@gmail.com"
    fi
    
    # Step 3: Add all files
    print_info "Adding all files to staging area..."
    git add .
    print_success "All files added"
    
    # Step 4: Check for changes
    if git diff --cached --quiet; then
        print_warning "No changes to commit"
    else
        # Commit with message
        print_info "Creating commit..."
        git commit -m "Final Release: CryptoSentinel Framework v1.0 - Complete Suite"
        print_success "Commit created successfully"
    fi
    
    # Step 5: Add remote origin
    print_info "Adding remote origin..."
    if git remote | grep -q "origin"; then
        print_warning "Remote 'origin' already exists. Removing..."
        git remote remove origin
    fi
    git remote add origin "$REPO_URL"
    print_success "Remote origin added: $REPO_URL"
    
    # Step 6: Create main branch if needed
    print_info "Ensuring main branch exists..."
    CURRENT_BRANCH=$(git branch --show-current)
    if [ "$CURRENT_BRANCH" != "main" ]; then
        if git show-ref --verify --quiet refs/heads/main; then
            git checkout main
        else
            git branch -M main
        fi
    fi
    print_success "On branch: main"
    
    # Step 7: Force push to main
    print_info "Force pushing to remote (this will overwrite remote history)..."
    print_warning "This operation will replace all remote content!"
    
    # Push with force
    if git push -f origin main; then
        print_success "Code repository deployed successfully!"
    else
        print_error "Failed to push to remote repository"
        print_info "You may need to authenticate with GitHub"
        print_info "Please ensure you have proper access rights to the repository"
        exit 1
    fi
    
    echo -e "${GREEN}${BOLD}"
    echo "═══════════════════════════════════════════════════════════════════════════"
    echo "  ✓ CODE REPOSITORY DEPLOYMENT COMPLETE!"
    echo "═══════════════════════════════════════════════════════════════════════════"
    echo -e "${NC}"
}

# ═══════════════════════════════════════════════════════════════════════════
# PART B: DEPLOY WIKI DOCUMENTATION
# ═══════════════════════════════════════════════════════════════════════════

deploy_wiki() {
    print_step "PART B: DEPLOYING WIKI DOCUMENTATION"
    
    # Step 1: Create temporary directory
    print_info "Creating temporary wiki directory..."
    if [ -d "$TEMP_WIKI_DIR" ]; then
        print_warning "Temporary wiki directory exists. Removing..."
        rm -rf "$TEMP_WIKI_DIR"
    fi
    mkdir -p "$TEMP_WIKI_DIR"
    print_success "Temporary directory created: $TEMP_WIKI_DIR"
    
    # Step 2: Clone wiki repository
    print_info "Cloning wiki repository..."
    if git clone "$WIKI_URL" "$TEMP_WIKI_DIR" 2>/dev/null; then
        print_success "Wiki repository cloned successfully"
    else
        print_warning "Wiki repository doesn't exist yet. Initializing new wiki..."
        cd "$TEMP_WIKI_DIR"
        git init
        git remote add origin "$WIKI_URL"
        cd ..
    fi
    
    # Step 3: Copy all markdown files from wiki_docs/
    print_info "Copying wiki documentation files..."
    if [ -d "wiki_docs" ]; then
        cp wiki_docs/*.md "$TEMP_WIKI_DIR/" 2>/dev/null || true
        
        # Count files
        FILE_COUNT=$(find "$TEMP_WIKI_DIR" -maxdepth 1 -name "*.md" | wc -l)
        print_success "Copied $FILE_COUNT markdown files"
        
        # List copied files
        print_info "Files prepared for deployment:"
        for file in "$TEMP_WIKI_DIR"/*.md; do
            if [ -f "$file" ]; then
                echo -e "  ${CYAN}→ $(basename "$file")${NC}"
            fi
        done
    else
        print_error "wiki_docs directory not found!"
        cleanup_and_exit 1
    fi
    
    # Step 4: Commit wiki changes
    print_info "Committing wiki changes..."
    cd "$TEMP_WIKI_DIR"
    
    # Configure git if needed
    if [ -z "$(git config user.name)" ]; then
        git config user.name "Shiva-destroyer"
        git config user.email "saisrujanmurthy@gmail.com"
    fi
    
    git add *.md
    
    if git diff --cached --quiet; then
        print_warning "No changes to commit in wiki"
    else
        git commit -m "Update comprehensive documentation"
        print_success "Wiki commit created"
    fi
    
    # Step 5: Create main branch if needed
    CURRENT_BRANCH=$(git branch --show-current)
    if [ -z "$CURRENT_BRANCH" ]; then
        git checkout -b main
    elif [ "$CURRENT_BRANCH" != "main" ]; then
        if git show-ref --verify --quiet refs/heads/main; then
            git checkout main
        else
            git branch -M main
        fi
    fi
    
    # Step 6: Push to wiki repository
    print_info "Pushing wiki documentation to remote..."
    if git push -f origin main; then
        print_success "Wiki documentation deployed successfully!"
    else
        print_error "Failed to push wiki documentation"
        print_info "The wiki may need to be initialized manually from GitHub"
        cd ..
        cleanup_and_exit 1
    fi
    
    cd ..
    
    # Step 7: Cleanup
    print_info "Cleaning up temporary directory..."
    rm -rf "$TEMP_WIKI_DIR"
    print_success "Cleanup complete"
    
    echo -e "${GREEN}${BOLD}"
    echo "═══════════════════════════════════════════════════════════════════════════"
    echo "  ✓ WIKI DOCUMENTATION DEPLOYMENT COMPLETE!"
    echo "═══════════════════════════════════════════════════════════════════════════"
    echo -e "${NC}"
}

# ═══════════════════════════════════════════════════════════════════════════
# CLEANUP AND EXIT
# ═══════════════════════════════════════════════════════════════════════════

cleanup_and_exit() {
    EXIT_CODE=${1:-0}
    
    # Remove temporary wiki directory if it exists
    if [ -d "$TEMP_WIKI_DIR" ]; then
        print_info "Performing cleanup..."
        rm -rf "$TEMP_WIKI_DIR"
        print_success "Cleanup complete"
    fi
    
    exit $EXIT_CODE
}

# ═══════════════════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════

main() {
    print_banner
    
    # Show deployment information
    print_info "Repository URL: $REPO_URL"
    print_info "Wiki URL: $WIKI_URL"
    print_info "Current Directory: $(pwd)"
    
    echo -e "\n${YELLOW}${BOLD}⚠ WARNING: This script will force push to remote repositories!${NC}"
    echo -e "${YELLOW}   All remote history will be replaced with local content.${NC}"
    echo -e "\n${CYAN}Press CTRL+C within 5 seconds to cancel...${NC}\n"
    
    sleep 5
    
    # Execute deployment steps
    deploy_code
    deploy_wiki
    
    # Final success message
    echo -e "${GREEN}${BOLD}"
    echo "═══════════════════════════════════════════════════════════════════════════"
    echo "  🎉 DEPLOYMENT COMPLETE! 🎉"
    echo "═══════════════════════════════════════════════════════════════════════════"
    echo ""
    echo "  📦 Code Repository: https://github.com/Shiva-destroyer/CryptoSentinel"
    echo "  📚 Wiki Documentation: https://github.com/Shiva-destroyer/CryptoSentinel/wiki"
    echo ""
    echo "  Next Steps:"
    echo "    1. Visit the repository to verify deployment"
    echo "    2. Check the wiki for documentation"
    echo "    3. Share with the world! 🚀"
    echo ""
    echo "═══════════════════════════════════════════════════════════════════════════"
    echo -e "${NC}"
}

# Trap errors and cleanup
trap 'cleanup_and_exit 1' ERR INT TERM

# Run main function
main

exit 0
