#!/usr/bin/env python3
"""
Multi-Agent System Launcher
Simple launcher for the multi-agent AI system
"""

import sys
import os
import argparse
from pathlib import Path

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(description="Multi-Agent AI System Launcher")
    parser.add_argument('--mode', choices=['gui', 'cli', 'test'], default='gui',
                       help='Mode to run the system in (default: gui)')
    parser.add_argument('--request', type=str, help='Single request to process (CLI mode)')
    parser.add_argument('--test-type', choices=['quick', 'agents', 'coordination', 'tools', 'memory', 'errors', 'performance', 'all'],
                       default='quick', help='Test type to run (test mode)')
    
    args = parser.parse_args()
    
    # Add current directory to path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    if args.mode == 'gui':
        print("Starting Multi-Agent System GUI...")
        try:
            from user_interface import main as gui_main
            gui_main()
        except ImportError as e:
            print(f"Error importing GUI: {e}")
            print("Make sure tkinter is available and user_interface.py exists")
            sys.exit(1)
        except Exception as e:
            print(f"GUI Error: {e}")
            sys.exit(1)
    
    elif args.mode == 'cli':
        print("Starting Multi-Agent System CLI...")
        try:
            from main_system import MultiAgentSystem
            
            system = MultiAgentSystem()
            system.start_session("cli_user")
            
            if args.request:
                # Process single request
                print(f"Processing request: {args.request}")
                response = system.process_request(args.request)
                print(f"\nResponse:\n{response}")
            else:
                # Interactive CLI mode
                system.interactive_mode()
                
        except ImportError as e:
            print(f"Error importing system: {e}")
            print("Make sure main_system.py exists")
            sys.exit(1)
        except Exception as e:
            print(f"CLI Error: {e}")
            sys.exit(1)
    
    elif args.mode == 'test':
        print(f"Running tests: {args.test_type}")
        try:
            from test_agents import main as test_main
            
            # Set test type as command line argument
            sys.argv = ['test_agents.py', args.test_type]
            test_main()
            
        except ImportError as e:
            print(f"Error importing tests: {e}")
            print("Make sure test_agents.py exists")
            sys.exit(1)
        except Exception as e:
            print(f"Test Error: {e}")
            sys.exit(1)

def check_dependencies():
    """Check if all required dependencies are available"""
    print("Checking dependencies...")
    
    required_modules = [
        'tkinter',
        'google.generativeai',
        'dotenv',
        'requests',
        'json',
        'datetime',
        'threading',
        'queue'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"OK {module}")
        except ImportError:
            print(f"ERROR {module} - MISSING")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\nMissing modules: {', '.join(missing_modules)}")
        print("Please install missing dependencies:")
        print("pip install google-generativeai python-dotenv requests")
        return False
    else:
        print("\nAll dependencies available!")
        return True

def check_files():
    """Check if all required files exist"""
    print("\nChecking files...")
    
    required_files = [
        'main_system.py',
        'user_interface.py',
        'test_agents.py',
        'multi_agent_system/agents/manager_agent.py',
        'multi_agent_system/agents/writer_agent.py',
        'multi_agent_system/agents/critic_agent.py',
        'multi_agent_system/agents/researcher_agent.py',
        'multi_agent_system/agents/analyst_agent.py'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"OK {file_path}")
        else:
            print(f"ERROR {file_path} - MISSING")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\nMissing files: {', '.join(missing_files)}")
        return False
    else:
        print("\nAll files present!")
        return True

def setup_environment():
    """Setup environment variables"""
    print("\nSetting up environment...")
    
    # Check for .env file
    if not os.path.exists('.env'):
        print("No .env file found")
        print("Please create a .env file with your Google API key:")
        print("GOOGLE_API_KEY=your_api_key_here")
        return False
    
    print(".env file found")
    return True

if __name__ == "__main__":
    # Check if help is requested
    if len(sys.argv) == 1 or '--help' in sys.argv or '-h' in sys.argv:
        print("Multi-Agent AI System Launcher")
        print("="*50)
        print("\nUsage:")
        print("  python run_system.py                    # Start GUI (default)")
        print("  python run_system.py --mode gui        # Start GUI")
        print("  python run_system.py --mode cli        # Start CLI")
        print("  python run_system.py --mode test       # Run tests")
        print("  python run_system.py --mode cli --request 'Your request here'")
        print("  python run_system.py --mode test --test-type all")
        print("\nModes:")
        print("  gui     - Graphical user interface (default)")
        print("  cli     - Command line interface")
        print("  test    - Run test suite")
        print("\nTest Types:")
        print("  quick       - Quick functionality test")
        print("  agents      - Test individual agents")
        print("  coordination - Test multi-agent coordination")
        print("  tools       - Test tools integration")
        print("  memory      - Test memory systems")
        print("  errors      - Test error handling")
        print("  performance - Test performance benchmarks")
        print("  all         - Run comprehensive test suite")
        print("\nExamples:")
        print("  python run_system.py --mode cli --request 'Create a blog post about AI'")
        print("  python run_system.py --mode test --test-type quick")
        print("\nDependencies:")
        print("  - tkinter (usually included with Python)")
        print("  - google-generativeai")
        print("  - python-dotenv")
        print("  - requests")
        print("\nSetup:")
        print("  1. Install dependencies: pip install google-generativeai python-dotenv requests")
        print("  2. Create .env file with: GOOGLE_API_KEY=your_api_key_here")
        print("  3. Run: python run_system.py")
        
        # Check dependencies and files
        print("\n" + "="*50)
        deps_ok = check_dependencies()
        files_ok = check_files()
        env_ok = setup_environment()
        
        if deps_ok and files_ok and env_ok:
            print("\nSystem is ready to run!")
        else:
            print("\nPlease fix the issues above before running the system.")
        
        sys.exit(0)
    
    # Run the main function
    main() 