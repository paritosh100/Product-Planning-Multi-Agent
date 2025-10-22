#!/usr/bin/env python3
"""
Quick setup script for CrewAI integration
Run this script to verify your environment is ready.
"""

import os
import sys
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("❌ .env file not found")
        print("\n📝 Creating .env template...")
        
        template = """# OpenAI API Configuration
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-api-key-here

# OpenAI Model Selection
# Options: gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo
OPENAI_MODEL=gpt-4o-mini
"""
        
        with open(".env", "w") as f:
            f.write(template)
        
        print("✅ .env file created!")
        print("⚠️  Please edit .env and add your OpenAI API key")
        return False
    
    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "sk-your-api-key-here":
        print("❌ OPENAI_API_KEY not set in .env")
        print("⚠️  Please edit .env and add your OpenAI API key")
        return False
    
    print("✅ .env file exists and API key is set")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required = {
        "streamlit": "streamlit",
        "crewai": "crewai",
        "openai": "openai",
        "pydantic": "pydantic",
        "dotenv": "python-dotenv",
        "pandas": "pandas",
    }
    
    missing = []
    
    for module, package in required.items():
        try:
            __import__(module)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} not installed")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Install missing packages:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    return True

def test_openai_connection():
    """Test OpenAI API connection"""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "sk-your-api-key-here":
        print("⚠️  Skipping API test (no valid key)")
        return False
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        print("🔄 Testing OpenAI API connection...")
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=4,
        )
        print("✅ OpenAI API connection successful!")
        return True
    except Exception as e:
        print(f"❌ OpenAI API test failed: {e}")
        return False

def main():
    print("=" * 60)
    print("CrewAI Integration Setup Checker")
    print("=" * 60)
    print()
    
    print("Step 1: Checking dependencies...")
    print("-" * 60)
    deps_ok = check_dependencies()
    print()
    
    print("Step 2: Checking environment configuration...")
    print("-" * 60)
    env_ok = check_env_file()
    print()
    
    if deps_ok and env_ok:
        print("Step 3: Testing OpenAI API...")
        print("-" * 60)
        api_ok = test_openai_connection()
        print()
    else:
        api_ok = False
    
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    
    if deps_ok and env_ok and api_ok:
        print("✅ All checks passed! CrewAI is ready to use.")
        print()
        print("🚀 Start your app with:")
        print("   streamlit run streamlit_app.py")
        print()
        print("💡 Remember to check 'Estimate hours' in the UI!")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print()
        if not deps_ok:
            print("📦 Install dependencies:")
            print("   pip install -r requirements.txt")
        if not env_ok:
            print("🔑 Add your OpenAI API key to .env file")
        print()
        print("📖 See CREWAI_INTEGRATION_GUIDE.md for detailed instructions")
    
    print("=" * 60)

if __name__ == "__main__":
    main()

