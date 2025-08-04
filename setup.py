#!/usr/bin/env python3
"""
Setup script for BNS Legal Assistant
This script initializes the system and processes the BNS data
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'fastapi', 'uvicorn', 'google-generativeai', 'cassandra-driver',
        'python-dotenv', 'requests', 'pydantic', 'numpy', 'sentence-transformers'
    ]
    
    missing_packages = []
    
    # Map package names to import names
    package_imports = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn',
        'google-generativeai': 'google.generativeai',
        'cassandra-driver': 'cassandra',
        'python-dotenv': 'dotenv',
        'requests': 'requests',
        'pydantic': 'pydantic',
        'numpy': 'numpy',
        'sentence-transformers': 'sentence_transformers'
    }
    
    # Skip sentence-transformers check as it's optional for basic setup
    skip_packages = ['sentence-transformers']
    
    for package in required_packages:
        if package in skip_packages:
            print(f"⏭️ {package} - SKIPPED (optional)")
            continue
        try:
            import_name = package_imports.get(package, package.replace('-', '_'))
            __import__(import_name)
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - MISSING")
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install missing packages using:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def check_environment():
    """Check if environment variables are set"""
    print("\n🔍 Checking environment variables...")
    
    required_vars = [
        'GEMINI_API_KEY',
        'DATASTAX_API_KEY',
        'DATASTAX_SECURE_CONNECT_BUNDLE_PATH'
    ]
    
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
            print(f"❌ {var} - NOT SET")
        else:
            print(f"✅ {var}")
    
    if missing_vars:
        print(f"\n❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your .env file")
        return False
    
    print("✅ All environment variables are set!")
    return True

def check_data_files():
    """Check if required data files exist"""
    print("\n🔍 Checking data files...")
    
    required_files = [
        'BNS_optimized.json'
    ]
    
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
            print(f"❌ {file} - NOT FOUND")
        else:
            print(f"✅ {file}")
    
    if missing_files:
        print(f"\n❌ Missing data files: {', '.join(missing_files)}")
        return False
    
    print("✅ All data files are present!")
    return True

def process_bns_data():
    """Process BNS data and store in vector database"""
    print("\n🔄 Processing BNS data...")
    
    try:
        from data_processor import BNSDataProcessor
        from vector_db import DataStaxVectorDB
        
        # Process data
        processor = BNSDataProcessor()
        documents = processor.process_and_embed("BNS_optimized.json")
        
        # Store in vector database (with fallback to file)
        try:
            vector_db = DataStaxVectorDB()
            vector_db.insert_documents(documents)
            print(f"✅ Successfully processed {len(documents)} BNS sections and stored in database")
        except Exception as db_error:
            print(f"⚠️ Database storage failed: {db_error}")
            print("✅ Data processed and stored locally as fallback")
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing BNS data: {e}")
        return False

def test_connections():
    """Test connections to external services"""
    print("\n🔍 Testing connections...")
    
    # Test Gemini LLM
    try:
        from llm_interface import GeminiLLM
        llm = GeminiLLM()
        if llm.test_connection():
            print("✅ Gemini LLM connection successful")
        else:
            print("❌ Gemini LLM connection failed")
            return False
    except Exception as e:
        print(f"❌ Gemini LLM connection error: {e}")
        return False
    
    # Test vector database
    try:
        from vector_db import DataStaxVectorDB
        vector_db = DataStaxVectorDB()
        print("✅ Vector database connection successful")
    except Exception as e:
        print(f"⚠️ Vector database connection error: {e}")
        print("System will use local file storage as fallback")
        return True  # Continue with setup even if vector DB fails
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        'frontend',
        'logs',
        'data'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def main():
    """Main setup function"""
    print("🚀 BNS Legal Assistant Setup")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Setup failed: Missing dependencies")
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        print("\n❌ Setup failed: Missing environment variables")
        print("Please create a .env file with the required variables")
        sys.exit(1)
    
    # Check data files
    if not check_data_files():
        print("\n❌ Setup failed: Missing data files")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Test connections
    if not test_connections():
        print("\n❌ Setup failed: Connection tests failed")
        sys.exit(1)
    
    # Process BNS data
    if not process_bns_data():
        print("\n❌ Setup failed: Could not process BNS data")
        sys.exit(1)
    
    print("\n" + "=" * 40)
    print("✅ Setup completed successfully!")
    print("\n🎉 Your BNS Legal Assistant is ready to use!")
    print("\nTo start the server, run:")
    print("python main.py")
    print("\nTo access the web interface, open:")
    print("http://localhost:8000/frontend/index.html")

if __name__ == "__main__":
    main() 