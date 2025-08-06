"""
Installation script for Multi-Agent AI System
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        return False
    print(f"Python version: {sys.version}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    if not env_file.exists():
        print("Creating .env file...")
        env_content = """# Multi-Agent AI System Configuration
# Add your Google API key here
GOOGLE_API_KEY=your_google_api_key_here

# Optional: Configure other settings
DEBUG=False
LOG_LEVEL=INFO
"""
        env_file.write_text(env_content)
        print(".env file created. Please add your Google API key.")
        return False
    else:
        print(".env file already exists.")
        return True

def check_env_configuration():
    """Check if .env file is properly configured"""
    env_file = Path(".env")
    if not env_file.exists():
        return False
    
    content = env_file.read_text()
    if "your_google_api_key_here" in content:
        print("Warning: Please update your Google API key in .env file")
        return False
    
    return True

def run_tests():
    """Run basic tests to verify installation"""
    print("Running basic tests...")
    
    try:
        result = subprocess.run([sys.executable, "quick_test.py"], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print("Tests passed!")
            return True
        else:
            print("Tests failed. Check the output above.")
            return False
    except subprocess.TimeoutExpired:
        print("Tests timed out. This might be normal if API calls are slow.")
        return True
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

def main():
    """Main installation function"""
    print("Multi-Agent AI System - Installation")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("Failed to install dependencies. Please check your internet connection.")
        sys.exit(1)
    
    # Create .env file
    env_configured = create_env_file()
    
    # Check environment configuration
    if not check_env_configuration():
        print("\nSetup Instructions:")
        print("1. Edit the .env file and add your Google API key")
        print("2. Get your API key from: https://makersuite.google.com/app/apikey")
        print("3. Replace 'your_google_api_key_here' with your actual API key")
        print("4. Run: python run_system.py")
    
    # Run tests
    if env_configured:
        if not run_tests():
            print("Warning: Tests failed. The system might not work properly.")
    
    print("\nInstallation completed!")
    print("\nNext steps:")
    print("1. Configure your .env file with your Google API key")
    print("2. Run the system: python run_system.py")
    print("3. Or use the GUI: python user_interface.py")
    print("4. Or run tests: python test_agents.py")

if __name__ == "__main__":
    main() 