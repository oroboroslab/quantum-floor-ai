"""
AXIS-7B-C Setup Script
"""

from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory.parent / "DOCUMENTATION" / "README.md").read_text()

setup(
    name="axis-7b-c",
    version="1.0.0",
    author="Oroboros Labs",
    author_email="oroboros.lab.q@gmail.com",
    description="AXIS-7B-C: 48MB ultra-fast encrypted model with <20ms latency",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oroboroslab/quantum-floor-ai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "cryptography>=41.0.0",
    ],
    extras_require={
        "gpu": ["torch>=2.0.0"],
        "npu": ["openvino>=2023.0.0"],
        "dev": ["pytest>=7.0.0", "pytest-benchmark>=4.0.0"],
    },
    include_package_data=True,
    package_data={
        "": ["*.bin", "*.bin.enc", "*.gguf.enc", "*.key"],
    },
)
