"""
nex-shared package setup
Shared components for NEX Automat applications
"""

from setuptools import setup

setup(
    name="nex-shared",
    version="1.0.0",
    description="Shared components for NEX Automat applications",
    author="ICC Komárno",
    python_requires=">=3.8",
    # Map nex_shared namespace to current directory (FLAT structure)
    package_dir={"nex_shared": "."},
    # Define packages with nex_shared namespace
    packages=[
        "nex_shared.ui",
        "nex_shared.database",
        "nex_shared.utils",
    ],
    # Include package data
    package_data={
        "nex_shared.ui": ["*.py"],
        "nex_shared.database": ["*.py"],
        "nex_shared.utils": ["*.py"],
    },
    # Dependencies
    install_requires=[
        "PyQt5>=5.15.0",
    ],
    # Development dependencies
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-qt>=4.0.0",
        ],
    },
    # Project URLs
    url="https://github.com/rauschiccsk/nex-automat",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
