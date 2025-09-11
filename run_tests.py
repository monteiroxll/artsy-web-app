#!/usr/bin/env python3
"""
Test runner script for the Artsy Web Service.
Provides easy commands to run different types of tests.
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=False)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False


def main():
    """Main test runner function."""
    if len(sys.argv) < 2:
        print("Usage: python run_tests.py [command]")
        print("\nAvailable commands:")
        print("  unit       - Run unit tests only")
        print("  integration - Run integration tests only")
        print("  all        - Run all tests")
        print("  coverage   - Run tests with coverage report")
        print("  install    - Install test dependencies")
        print("  lint       - Run code linting")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    # Change to the app directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    if command == "install":
        success = run_command(
            "pip install -r requirements.txt",
            "Installing dependencies"
        )
    
    elif command == "unit":
        success = run_command(
            "python -m pytest tests/test_main.py::TestArtsyWebService -v",
            "Running unit tests"
        )
    
    elif command == "integration":
        success = run_command(
            "python -m pytest tests/test_main.py::TestIntegration -v",
            "Running integration tests"
        )
    
    elif command == "all":
        success = run_command(
            "python -m pytest tests/ -v",
            "Running all tests"
        )
    
    elif command == "coverage":
        success = run_command(
            "python -m pytest tests/ --cov=main --cov-report=term-missing --cov-report=html",
            "Running tests with coverage"
        )
        if success:
            print("\n📊 Coverage report generated in htmlcov/index.html")
    
    elif command == "lint":
        success = run_command(
            "python -m flake8 main.py tests/ --max-line-length=100",
            "Running code linting"
        )
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)
    
    if not success:
        sys.exit(1)
    
    print(f"\n🎉 {command.title()} completed successfully!")


if __name__ == "__main__":
    main()
