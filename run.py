#!/usr/bin/env python3
"""
Language Learning Buddy - Startup Script
Run this script to start the application
"""

import os
import sys
import uvicorn
from pathlib import Path

def check_env():
    """Check if GROQ_API_KEY is set"""
    if not os.getenv("GROQ_API_KEY"):
        print("❌ Error: GROQ_API_KEY environment variable is not set!")
        print("\nPlease set your Groq API key:")
        print("Windows: set GROQ_API_KEY=your_api_key_here")
        print("Linux/Mac: export GROQ_API_KEY=your_api_key_here")
        print("\nOr create a .env file with: GROQ_API_KEY=your_api_key_here")
        return False
    return True

def main():
    """Main function to start the application"""
    print("🌍 Starting Language Learning Buddy...")
    
    # Check if API key is set
    if not check_env():
        sys.exit(1)
    
    # Check if required directories exist
    required_dirs = ["static/audio", "templates", "tools"]
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            print(f"❌ Error: Required directory '{dir_path}' not found!")
            sys.exit(1)
    
    print("✅ All checks passed!")
    print("🚀 Starting server at http://127.0.0.1:8000")
    print("📖 Open your browser and start learning!")
    print("\nPress Ctrl+C to stop the server")
    
    # Start the server
    try:
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Goodbye! Thanks for using Language Learning Buddy!")

if __name__ == "__main__":
    main()
