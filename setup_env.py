#!/usr/bin/env python3
"""
Environment Setup Script for BNS Legal Assistant
This script helps you set up your .env file with the correct API keys
"""

import os
import secrets
from pathlib import Path

def generate_secret_key():
    """Generate a secure random secret key"""
    return secrets.token_urlsafe(32)

def create_env_file():
    """Create .env file with user input"""
    print("🚀 BNS Legal Assistant Environment Setup")
    print("=" * 50)
    
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
    
    # Get DataStax Database ID
    print("\n🔑 DataStax Database ID:")
    print("This is the ID from your database URL")
    print("Example: If your URL is https://08c510a2-4520-404f-89ef-1eedb61ba195-us-east-2.apps.astra.datastax.com")
    print("Then your Database ID is: 08c510a2-4520-404f-89ef-1eedb61ba195")
    datastax_db_id = input("Enter your DataStax Database ID: ").strip()
    
    # Generate secret key
    secret_key = generate_secret_key()
    
    # Create .env content
    env_content = f"""# BNS Legal Assistant Environment Configuration
# =============================================

# Gemini API Configuration
# Get your API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY={gemini_key or 'your_gemini_api_key_here'}

# DataStax Astra DB Configuration (REST API)
# Get your API token from: https://astra.datastax.com/
DATASTAX_API_KEY={datastax_token or 'your_datastax_api_token_here'}
DATASTAX_DATABASE_ID={datastax_db_id or 'your_database_id_here'}

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
        if not datastax_db_id:
            missing.append("DataStax Database ID")
        
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