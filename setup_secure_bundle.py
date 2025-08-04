#!/usr/bin/env python3
"""
Secure Connect Bundle Setup Script for BNS Legal Assistant
This script helps you set up your .env file with the secure connect bundle
"""

import os
import secrets
from pathlib import Path

def generate_secret_key():
    """Generate a secure random secret key"""
    return secrets.token_urlsafe(32)

def create_env_file():
    """Create .env file with user input"""
    print("🚀 BNS Legal Assistant Environment Setup (Secure Connect Bundle)")
    print("=" * 60)
    
    # Check if .env already exists
    if Path(".env").exists():
        print("⚠️ .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ").lower()
        if response != 'y':
            print("Setup cancelled.")
            return
    
    print("\n📝 Please provide the following information:")
    print("(Press Enter to skip any field you want to fill later)")
    
    # Get Gemini API Key
    print("\n🔑 Gemini API Key:")
    print("Get your API key from: https://makersuite.google.com/app/apikey")
    gemini_key = input("Enter your Gemini API key: ").strip()
    
    # Get DataStax API Token
    print("\n🔑 DataStax API Token:")
    print("Get your API token from: https://astra.datastax.com/")
    print("1. Go to your database dashboard")
    print("2. Click 'Settings' → 'API Keys'")
    print("3. Create a new API key")
    print("4. Copy the Client ID")
    datastax_token = input("Enter your DataStax API token: ").strip()
    
    # Get Secure Connect Bundle path
    print("\n📁 Secure Connect Bundle:")
    print("This should be the path to your downloaded secure connect bundle ZIP file")
    print("Example: secure-connect-your-database.zip")
    secure_bundle = input("Enter the path to your secure connect bundle: ").strip()
    
    # Generate secret key
    secret_key = generate_secret_key()
    
    # Create .env content
    env_content = f"""# BNS Legal Assistant Environment Configuration
# =============================================

# Gemini API Configuration
# Get your API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY={gemini_key or 'your_gemini_api_key_here'}

# DataStax Astra DB Configuration (Secure Connect Bundle)
# Get your API token from: https://astra.datastax.com/
DATASTAX_API_KEY={datastax_token or 'your_datastax_api_token_here'}
DATASTAX_SECURE_CONNECT_BUNDLE_PATH={secure_bundle or 'your_secure_connect_bundle.zip'}

# Application Security
SECRET_KEY={secret_key}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Optional: Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/bns_legal_assistant.log
"""
    
    # Write .env file
    try:
        with open(".env", "w") as f:
            f.write(env_content)
        
        print("\n✅ .env file created successfully!")
        print(f"📁 File location: {Path('.env').absolute()}")
        
        # Check what's missing
        missing = []
        if not gemini_key:
            missing.append("Gemini API Key")
        if not datastax_token:
            missing.append("DataStax API Token")
        if not secure_bundle:
            missing.append("Secure Connect Bundle path")
        
        if missing:
            print(f"\n⚠️ You still need to set: {', '.join(missing)}")
            print("Edit the .env file to add these values.")
        else:
            print("\n🎉 All API keys are configured!")
            print("You can now run: python setup.py")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

def main():
    """Main function"""
    create_env_file()

if __name__ == "__main__":
    main() 