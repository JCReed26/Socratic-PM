#!/usr/bin/env python3
"""
Zero-LLM telemetry script. Gathers environment state deterministically.
Returns JSON with: git branch, uncommitted changes count, Python version, Node version, installed packages.
"""

import json
import subprocess
import sys


def get_git_info():
    """Get current git branch and uncommitted changes count."""
    try:
        branch = (
            subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"], stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )
    except subprocess.CalledProcessError:
        branch = None

    try:
        status_output = (
            subprocess.check_output(
                ["git", "status", "--porcelain"], stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )
        uncommitted_changes = len([line for line in status_output.split("\n") if line])
    except subprocess.CalledProcessError:
        uncommitted_changes = None

    return {"branch": branch, "uncommitted_changes": uncommitted_changes}


def get_python_version():
    """Get Python version."""
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def get_node_version():
    """Get Node.js version."""
    try:
        version = (
            subprocess.check_output(["node", "--version"], stderr=subprocess.DEVNULL)
            .decode()
            .strip()
        )
        return version  # Returns "v20.x.x" format
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_installed_packages():
    """Get list of top 10 most important packages (by import frequency)."""
    packages = []
    important_packages = [
        "pip",
        "setuptools",
        "wheel",
        "langgraph",
        "langchain",
        "fastapi",
        "pydantic",
        "sqlalchemy",
        "psycopg",
        "pytest",
    ]

    for pkg in important_packages:
        try:
            result = subprocess.check_output(
                [sys.executable, "-m", "pip", "show", pkg], stderr=subprocess.DEVNULL
            ).decode()
            for line in result.split("\n"):
                if line.startswith("Version:"):
                    version = line.split("Version: ")[1].strip()
                    packages.append({"name": pkg, "version": version})
                    break
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

    return packages


def main():
    """Gather telemetry and output JSON."""
    telemetry = {
        "git": get_git_info(),
        "python_version": get_python_version(),
        "node_version": get_node_version(),
        "packages": get_installed_packages(),
    }
    print(json.dumps(telemetry, indent=2))


if __name__ == "__main__":
    main()
