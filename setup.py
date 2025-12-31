"""
CryptoSentinel Setup Configuration

Developer: saisrujanmurthy@gmail.com
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read long description from README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="crypto-sentinel",
    version="1.0.0",
    author="Sai Srujan Murthy",
    author_email="saisrujanmurthy@gmail.com",
    description="A production-grade cryptographic framework unifying 10+ security tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/CryptoSentinel",
    packages=find_packages(exclude=["tests", "tests.*", "docs"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Typing :: Typed",
    ],
    python_requires=">=3.10",
    install_requires=[
        "rich>=13.0.0",
        "click>=8.1.0",
        "typing-extensions>=4.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "mypy>=1.5.0",
            "black>=23.7.0",
            "ruff>=0.0.285",
            "isort>=5.12.0",
        ],
        "docs": [
            "sphinx>=7.1.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "crypto-sentinel=crypto_sentinel.ui.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "cryptography",
        "encryption",
        "security",
        "hashing",
        "cipher",
        "password",
        "analysis",
    ],
)
