#!/usr/bin/env python3
"""
Bitbucket PR Reviewer MCP Server - Python Package Setup
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="bitbucket-pr-reviewer-mcp",
    version="1.0.0",
    description="MCP Server for Bitbucket Pull Request Reviewing with AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="MdMugish",
    author_email="mugish@example.com",
    url="https://github.com/MdMugish/bitbucket-pr-reviewer-mcp",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "bitbucket-pr-reviewer-mcp=src.main:main",
        ],
    },
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
    keywords="mcp bitbucket pull-request review ai code-review",
    project_urls={
        "Bug Reports": "https://github.com/MdMugish/bitbucket-pr-reviewer-mcp/issues",
        "Source": "https://github.com/MdMugish/bitbucket-pr-reviewer-mcp",
        "Documentation": "https://github.com/MdMugish/bitbucket-pr-reviewer-mcp#readme",
    },
)
