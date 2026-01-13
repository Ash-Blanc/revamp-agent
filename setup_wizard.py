#!/usr/bin/env python3
"""
Interactive setup wizard for Revamp Agent.
Makes the initial setup process much more user-friendly.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Optional
import subprocess
import webbrowser

def print_banner():
    print("""
🚀 Revamp Agent Setup Wizard
============================
Transform your GitHub projects into hackathon winners!

This wizard will help you:
1. Install dependencies
2. Configure API keys
3. Test your setup
4. Run your first revamp
""")

def check_python_version():
    """Check if Python 3.13+ is installed."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 13):
        print("❌ Python 3.13+ required. Please upgrade Python.")
        return False
    print(f"✅ Python {version.major}.{version.minor} detected")
    return True

def install_uv():
    """Install uv package manager if not present."""
    try:
        subprocess.run(["uv", "--version"], capture_output=True, check=True)
        print("✅ uv package manager found")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("📦 Installing uv package manager...")
        try:
            if os.name == 'nt':  # Windows
                subprocess.run(["powershell", "-c", "irm https://astral.sh/uv/install.ps1 | iex"], check=True)
            else:  # Unix-like
                subprocess.run(["curl", "-LsSf", "https://astral.sh/uv/install.sh", "|", "sh"], shell=True, check=True)
            print("✅ uv installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install uv. Please install manually: https://docs.astral.sh/uv/")
            return False

def get_api_keys() -> Dict[str, str]:
    """Interactive API key collection with helpful guidance."""
    keys = {}
    
    print("\n🔑 API Key Configuration")
    print("=" * 30)
    
    # Essential keys
    print("\n📋 REQUIRED API Keys:")
    
    # OpenAI (most common)
    keys['OPENAI_API_KEY'] = input("OpenAI API Key (get from https://platform.openai.com/api-keys): ").strip()
    
    # LangWatch
    print("\n🔍 LangWatch (for prompt management):")
    print("Sign up at: https://app.langwatch.ai/")
    keys['LANGWATCH_API_KEY'] = input("LangWatch API Key: ").strip()
    
    print("\n📋 OPTIONAL API Keys (press Enter to skip):")
    
    # Firecrawl
    print("\n🕷️  Firecrawl (for web scraping hackathon sites):")
    print("Sign up at: https://firecrawl.dev/")
    firecrawl = input("Firecrawl API Key (optional): ").strip()
    if firecrawl:
        keys['FIRECRAWL_API_KEY'] = firecrawl
    
    # GitHub
    print("\n🐙 GitHub (for code implementation):")
    print("Create token at: https://github.com/settings/tokens")
    github = input("GitHub Access Token (optional): ").strip()
    if github:
        keys['GITHUB_ACCESS_TOKEN'] = github
    
    # Coding models
    print("\n🤖 Coding Models (optional, improves code generation):")
    
    cerebras = input("Cerebras API Key (recommended): ").strip()
    if cerebras:
        keys['CEREBRAS_API_KEY'] = cerebras
    
    mistral = input("Mistral API Key (fallback): ").strip()
    if mistral:
        keys['MISTRAL_API_KEY'] = mistral
    
    return keys

def create_env_file(keys: Dict[str, str]):
    """Create .env file with provided keys."""
    env_content = []
    for key, value in keys.items():
        if value:
            env_content.append(f"{key}={value}")
    
    with open('.env', 'w') as f:
        f.write('\n'.join(env_content))
    
    print("✅ .env file created")

def install_dependencies():
    """Install project dependencies."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.run(["uv", "sync"], check=True)
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def test_setup():
    """Test the setup by running a simple command."""
    print("\n🧪 Testing setup...")
    try:
        result = subprocess.run(["uv", "run", "python", "-c", "from app.main import revamp_project; print('✅ Setup working!')"], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Setup test failed: {e.stderr}")
        return False

def run_first_example():
    """Guide user through first example."""
    print("\n🎯 Ready to run your first revamp!")
    print("Let's try the discovery mode (no URLs needed):")
    
    topic = input("Enter a topic to search for (e.g., 'AI', 'web3', 'climate'): ").strip() or "AI"
    
    print(f"\n🔍 Searching for {topic} projects and hackathons...")
    print("Command: revamp analyze --topic", topic)
    
    try:
        subprocess.run(["uv", "run", "revamp", "analyze", "--topic", topic], check=True)
        print("\n🎉 Success! Your first revamp analysis is complete!")
    except subprocess.CalledProcessError:
        print("❌ Example failed. Check your API keys and try again.")

def main():
    """Main setup wizard flow."""
    print_banner()
    
    # Check prerequisites
    if not check_python_version():
        return
    
    if not install_uv():
        return
    
    # Get API keys
    keys = get_api_keys()
    create_env_file(keys)
    
    # Install and test
    if not install_dependencies():
        return
    
    if not test_setup():
        print("\n⚠️  Setup test failed, but you can still try using the tool.")
    
    # First example
    run_example = input("\n🚀 Run a quick example? (y/n): ").strip().lower()
    if run_example in ['y', 'yes']:
        run_first_example()
    
    print("""
🎉 Setup Complete!

Next steps:
1. Try: revamp analyze --github <repo-url> --hackathon <hackathon-url>
2. Try: revamp generate --topic "AI" --fork
3. Read the docs: README.md
4. Join our community: [add community link]

Happy hacking! 🚀
""")

if __name__ == "__main__":
    main()