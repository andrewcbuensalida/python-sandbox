#!/usr/bin/env python3
"""
Development script for running the Flask application with uv
"""
import subprocess
import sys


def run_flask():
    """Run the Flask application using uv"""
    try:
        subprocess.run(
            [
                "uv",
                "run",
                "flask",
                "--app",
                "flask_world",
                "run",
                "--debug",
                "--host",
                "127.0.0.1",
                "--port",
                "5000",
            ],
            check=True,
        )
    except KeyboardInterrupt:
        print("\n🛑 Flask server stopped")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Flask: {e}")
        sys.exit(1)


if __name__ == "__main__":
    print("🚀 Starting Flask development server with uv...")
    run_flask()
