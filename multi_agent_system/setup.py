"""
Setup script for Multi-Agent AI System
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="multi-agent-ai-system",
    version="1.0.0",
    author="Ali Arslan",
    author_email="ali3dev@gmail.com",
    description="A robust multi-agent AI system with enhanced error handling and content generation",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/ali3dev/agentic-ai-by-aliarslan.git",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "multi-agent-system=run_system:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 