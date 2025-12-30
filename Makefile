# CryptoSentinel Makefile
# Author: saisrujanmurthy@gmail.com

.PHONY: help install test coverage lint format typecheck clean docs all

# Default target
help:
	@echo "╔═══════════════════════════════════════════════════════════╗"
	@echo "║         CryptoSentinel Development Commands              ║"
	@echo "╚═══════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Setup:"
	@echo "  make install      Install dependencies"
	@echo "  make install-dev  Install with dev dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test         Run all tests"
	@echo "  make coverage     Run tests with coverage report"
	@echo "  make test-verbose Run tests with verbose output"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint         Run linting checks"
	@echo "  make format       Format code with black and isort"
	@echo "  make typecheck    Run mypy type checking"
	@echo "  make check        Run all quality checks"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean        Remove build artifacts"
	@echo "  make docs         Generate documentation"
	@echo "  make all          Run format, lint, typecheck, test"
	@echo ""

# Installation
install:
	@echo "📦 Installing CryptoSentinel..."
	pip install -r requirements.txt
	pip install -e .
	@echo "✅ Installation complete!"

install-dev:
	@echo "📦 Installing CryptoSentinel with dev dependencies..."
	pip install -r requirements.txt
	pip install -e ".[dev]"
	@echo "✅ Development installation complete!"

# Testing
test:
	@echo "🧪 Running tests..."
	pytest tests/ -v

test-verbose:
	@echo "🧪 Running tests (verbose)..."
	pytest tests/ -vv -s

coverage:
	@echo "📊 Running tests with coverage..."
	pytest tests/ --cov=crypto_sentinel --cov-report=term-missing --cov-report=html
	@echo "✅ Coverage report generated in htmlcov/"

# Code Quality
lint:
	@echo "🔍 Running linting checks..."
	@echo "  → Ruff..."
	ruff check crypto_sentinel/
	@echo "✅ Linting complete!"

format:
	@echo "🎨 Formatting code..."
	@echo "  → Black..."
	black crypto_sentinel/ tests/
	@echo "  → isort..."
	isort crypto_sentinel/ tests/
	@echo "✅ Formatting complete!"

typecheck:
	@echo "🔎 Running type checks..."
	mypy crypto_sentinel/
	@echo "✅ Type checking complete!"

check: format lint typecheck
	@echo "✅ All quality checks passed!"

# Cleanup
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "✅ Cleanup complete!"

# Documentation
docs:
	@echo "📚 Documentation files:"
	@ls -lh docs/
	@echo ""
	@echo "📄 Main README:"
	@head -20 README.md

# All checks
all: format lint typecheck test
	@echo "╔═══════════════════════════════════════════════════════════╗"
	@echo "║              All Checks Completed Successfully!           ║"
	@echo "╚═══════════════════════════════════════════════════════════╝"

# Quick validation
validate:
	@echo "✓ Validating CryptoSentinel installation..."
	@python3 -c "from crypto_sentinel.core import CipherInterface, HasherInterface, AnalyzerInterface; print('✅ Core modules OK')"
	@python3 -c "from crypto_sentinel.utils.math_helpers import gcd, modular_inverse, calculate_ioc; print('✅ Math utilities OK')"
	@python3 -c "from crypto_sentinel.core.exceptions import CryptoSentinelError; print('✅ Exceptions OK')"
	@echo "🎉 CryptoSentinel is ready!"

# Info
info:
	@echo "╔═══════════════════════════════════════════════════════════╗"
	@echo "║              CryptoSentinel Project Info                 ║"
	@echo "╚═══════════════════════════════════════════════════════════╝"
	@echo "Author: Sai Srujan Murthy"
	@echo "Email:  saisrujanmurthy@gmail.com"
	@echo "Path:   $(PWD)"
	@echo ""
	@echo "Python Version:"
	@python3 --version
	@echo ""
	@echo "Project Structure:"
	@find crypto_sentinel -name "*.py" | head -10
	@echo "... (use 'tree' for full structure)"
