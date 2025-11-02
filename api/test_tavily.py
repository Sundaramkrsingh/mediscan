"""
Quick test to verify Tavily API configuration
Run this after activating virtual environment: venv\\Scripts\\activate
"""

import os
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Manually read .env file (simpler than using dotenv)
tavily_key = None
try:
    with open('.env', 'r') as f:
        for line in f:
            if line.startswith('TAVILY_API_KEY='):
                tavily_key = line.split('=', 1)[1].strip()
                break
except FileNotFoundError:
    print("[X] .env file not found!")
    print("Create a .env file in the api/ directory")
    exit(1)

# Check if Tavily is configured

if tavily_key:
    print("[OK] Tavily API key found!")
    print(f"     Key starts with: {tavily_key[:10]}...")
    print(f"     Key length: {len(tavily_key)} characters")

    # Try to initialize the service
    try:
        from tavily import TavilyClient
        client = TavilyClient(api_key=tavily_key)
        print("\n[OK] Tavily client initialized successfully!")
        print("\n==> Your Tavily setup is CORRECT!")
        print("\nNow when you run the backend (python main.py), it will use Tavily for real verification.")

    except ImportError:
        print("\n[!] Tavily package not installed")
        print("Run: pip install tavily-python")
    except Exception as e:
        print(f"\n[!] Error initializing Tavily: {e}")
else:
    print("[X] Tavily API key not found in .env file")
    print("Add this to api/.env:")
    print("TAVILY_API_KEY=your_key_here")
