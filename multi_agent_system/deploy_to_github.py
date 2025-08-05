#!/usr/bin/env python3
"""
Deployment script for uploading to GitHub repository
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"Success: {description}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {description}")
        print(f"Command: {command}")
        print(f"Error: {e.stderr}")
        return False

def check_git_installed():
    """Check if git is installed"""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: Git is not installed or not in PATH")
        return False

def initialize_git_repo():
    """Initialize git repository if not already done"""
    if not os.path.exists(".git"):
        print("Initializing git repository...")
        if not run_command("git init", "Initialize git repository"):
            return False
    return True

def add_files_to_git():
    """Add all files to git"""
    files_to_add = [
        "main_system.py",
        "user_interface.py",
        "run_system.py",
        "test_agents.py",
        "quick_test.py",
        "test_improvements.py",
        "demo_system.py",
        "setup.py",
        "requirements.txt",
        "README.md",
        ".gitignore",
        "multi_agent_system/",
        "interview_prep.py"
    ]
    
    for file_path in files_to_add:
        if os.path.exists(file_path):
            if not run_command(f"git add {file_path}", f"Add {file_path} to git"):
                return False
    
    return True

def commit_changes():
    """Commit changes with a descriptive message"""
    commit_message = "Add Multi-Agent AI System with enhanced error handling and content generation"
    return run_command(f'git commit -m "{commit_message}"', "Commit changes")

def add_remote_repository():
    """Add the GitHub repository as remote"""
    repo_url = "https://github.com/ali3dev/agentic-ai-by-aliarslan.git"
    return run_command(f"git remote add origin {repo_url}", "Add remote repository")

def push_to_github():
    """Push to GitHub"""
    return run_command("git push -u origin main", "Push to GitHub")

def main():
    """Main deployment function"""
    print("Multi-Agent AI System - GitHub Deployment")
    print("="*50)
    
    # Check if git is installed
    if not check_git_installed():
        sys.exit(1)
    
    # Initialize git repository
    if not initialize_git_repo():
        sys.exit(1)
    
    # Add files to git
    if not add_files_to_git():
        sys.exit(1)
    
    # Commit changes
    if not commit_changes():
        sys.exit(1)
    
    # Add remote repository
    if not add_remote_repository():
        sys.exit(1)
    
    # Push to GitHub
    if not push_to_github():
        print("\nManual steps required:")
        print("1. Go to https://github.com/ali3dev/agentic-ai-by-aliarslan")
        print("2. Create the repository if it doesn't exist")
        print("3. Follow the instructions to push your code")
        sys.exit(1)
    
    print("\nDeployment completed successfully!")
    print("Your project is now available at: https://github.com/ali3dev/agentic-ai-by-aliarslan")

if __name__ == "__main__":
    main() 