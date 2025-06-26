#!/usr/bin/env python3
"""Setup script for local installation of Deep Search MCP Server."""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command, check=True):
    """Run a command and handle errors."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        sys.exit(1)


def check_uv_installed():
    """Check if uv is installed."""
    try:
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"uv is installed: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("uv is not installed. Installing uv...")
    # Install uv using the official installer
    run_command("curl -LsSf https://astral.sh/uv/install.sh | sh")
    
    # Add uv to PATH for this session
    uv_bin = Path.home() / ".cargo" / "bin"
    if uv_bin.exists():
        os.environ["PATH"] = f"{uv_bin}:{os.environ.get('PATH', '')}"
    
    return True


def setup_project():
    """Set up the project with uv."""
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    print("Setting up Deep Search MCP Server locally...")
    
    # Check and install uv
    check_uv_installed()
    
    # Initialize uv project if needed
    if not Path("pyproject.toml").exists():
        print("pyproject.toml not found! Make sure you're in the correct directory.")
        sys.exit(1)
    
    # Install dependencies
    print("Installing dependencies with uv...")
    run_command("uv sync")
    
    # Install the package in development mode
    print("Installing package in development mode...")
    run_command("uv pip install -e .")
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        print("Creating .env file from template...")
        env_example = Path(".env.example")
        if env_example.exists():
            import shutil
            shutil.copy(env_example, env_file)
            print("✓ .env file created. Please edit it with your API keys.")
        else:
            # Create a basic .env file
            with open(env_file, "w") as f:
                f.write("""# Deep Search MCP Server Environment Variables

# Required: Google Gemini API Key
GOOGLE_API_KEY=your_google_api_key_here

# Required: Google Search API Key (choose one)
# Option 1: Google Serper (recommended - https://serper.dev)
SERPER_API_KEY=your_serper_api_key_here

# Option 2: SerpAPI (alternative - https://serpapi.com)
SERPAPI_API_KEY=your_serpapi_key_here

# Search configuration
MAX_SEARCH_RESULTS=10
MAX_RESEARCH_ITERATIONS=3
""")
            print("✓ Basic .env file created. Please edit it with your API keys.")
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Edit .env file with your API keys")
    print("2. Test the server:")
    print("   uv run python server.py")
    print("3. For Claude Desktop integration:")
    print("   mcp install server.py")
    print("4. For development:")
    print("   mcp dev server.py")


if __name__ == "__main__":
    setup_project()