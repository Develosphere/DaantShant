#!/usr/bin/env python3
"""
DaantShaant Setup Verification Script
Run this after setup to verify everything is working correctly.
"""

import asyncio
import json
import sys
from pathlib import Path
import subprocess
import requests
from urllib.parse import urljoin

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print("✅ Python version:", f"{version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print("❌ Python 3.11+ required, found:", f"{version.major}.{version.minor}.{version.micro}")
        return False

def check_file_exists(filepath, description):
    """Check if a file exists."""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} missing: {filepath}")
        return False

def check_env_file():
    """Check .env file and required variables."""
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ .env file not found. Copy .env.example to .env and configure API keys.")
        return False
    
    print("✅ .env file exists")
    
    # Check for required variables
    required_vars = [
        "TEETH_ANALYZER_GEMINI_API_KEY",
        "OPENROUTER_API_KEY",
        "MONGODB_URI",
        "MONGODB_DB"
    ]
    
    with open(env_path) as f:
        env_content = f.read()
    
    missing_vars = []
    for var in required_vars:
        if f"{var}=" not in env_content or f"{var}=your_" in env_content:
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing or placeholder API keys:", ", ".join(missing_vars))
        return False
    else:
        print("✅ All required environment variables configured")
        return True

def check_mongodb():
    """Check if MongoDB is running."""
    try:
        import pymongo
        client = pymongo.MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=2000)
        client.server_info()
        print("✅ MongoDB is running and accessible")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

def check_service(port, name):
    """Check if a service is running on the given port."""
    try:
        response = requests.get(f"http://127.0.0.1:{port}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ {name} service running on port {port}")
            return True
        else:
            print(f"❌ {name} service unhealthy on port {port}: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {name} service not accessible on port {port}: {e}")
        return False

def check_frontend():
    """Check if frontend is accessible."""
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend accessible on port 3000")
            return True
        else:
            print(f"❌ Frontend unhealthy on port 3000: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend not accessible on port 3000: {e}")
        return False

def main():
    """Run all verification checks."""
    print("🔍 DaantShaant Setup Verification")
    print("=" * 40)
    
    checks = [
        ("Python Version", check_python_version),
        ("Requirements File", lambda: check_file_exists("requirements.txt", "Requirements file")),
        ("Environment File", check_env_file),
        ("MongoDB", check_mongodb),
        ("Orchestrator Service", lambda: check_service(8000, "Orchestrator")),
        ("Teeth Analyzer Service", lambda: check_service(8001, "Teeth Analyzer")),
        ("Diagnosis Service", lambda: check_service(8002, "Diagnosis")),
        ("Frontend", check_frontend),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} check failed with error: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 40)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 40)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")
    
    print(f"\nResult: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! DaantShaant is ready to use.")
        print("\n🚀 Next steps:")
        print("   1. Open http://localhost:3000/chat")
        print("   2. Send a message to test conversational AI")
        print("   3. Upload a teeth image to test analysis")
        return True
    else:
        print(f"\n⚠️  {total - passed} checks failed. Please fix the issues above.")
        print("\n📖 For help, check:")
        print("   - README.md")
        print("   - SETUP_CHECKLIST.md")
        print("   - Terminal logs for error details")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)