#!/usr/bin/env python3
"""
Development workflow scripts using uv dependency groups
"""
import subprocess
import sys


def run_cmd(cmd):
    """Run a command and handle errors"""
    try:
        result = subprocess.run(
            cmd, shell=True, check=True, capture_output=True, text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False


def dev_setup():
    """Set up complete development environment"""
    print("🔧 Setting up development environment...")
    return run_cmd("uv sync --group dev --group test")


def run_tests():
    """Run tests with coverage"""
    print("🧪 Running tests with coverage...")
    return run_cmd("uv run pytest --cov=. --cov-report=html")


def format_code():
    """Format code using black and isort"""
    print("🎨 Formatting code...")
    success = True
    success &= run_cmd("uv run black .")
    success &= run_cmd("uv run isort .")
    return success


def lint_code():
    """Lint code using flake8 and mypy"""
    print("🔍 Linting code...")
    success = True
    success &= run_cmd("uv run flake8 .")
    success &= run_cmd("uv run mypy . --ignore-missing-imports")
    return success


def ci_pipeline():
    """Run full CI pipeline"""
    print("🚀 Running CI pipeline...")
    steps = [
        ("Setting up", dev_setup),
        ("Formatting", format_code),
        ("Linting", lint_code),
        ("Testing", run_tests),
    ]

    for step_name, step_func in steps:
        print(f"\n=== {step_name} ===")
        if not step_func():
            print(f"❌ {step_name} failed!")
            return False
        print(f"✅ {step_name} passed!")

    print("\n🎉 All steps completed successfully!")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts.py [dev-setup|test|format|lint|ci]")
        sys.exit(1)

    command = sys.argv[1]

    commands = {
        "dev-setup": dev_setup,
        "test": run_tests,
        "format": format_code,
        "lint": lint_code,
        "ci": ci_pipeline,
    }

    if command in commands:
        success = commands[command]()
        sys.exit(0 if success else 1)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
