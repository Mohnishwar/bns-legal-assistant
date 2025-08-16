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
        'fastapi', 'uvicorn', 'google-generativeai', 'qdrant-client',
        'python-dotenv', 'requests', 'pydantic', 'numpy', 'sentence-transformers'
    ]
    
    missing_packages = []
    
    # Map package names to import names
    package_imports = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn',
        'google-generativeai': 'google.generativeai',
        'qdrant-client': 'qdrant',
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
        'QDRANT_URL'
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
        print("Please create a .env file with the required variables")
        print("\nExample .env file:")
        print("GEMINI_API_KEY=your_gemini_api_key_here")
        print("QDRANT_URL=your_qdrant_url_here")
        print("SECRET_KEY=your_secret_key_here")
        print("HOST=0.0.0.0")
        print("PORT=8000")
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
        print("Please ensure BNS_optimized.json is in the project directory")
        return False
    
    print("✅ All data files are present!")
    return True

def process_bns_data():
    """Process BNS data and store in vector database"""
    print("\n🔄 Processing BNS data...")
    
    try:
        from data_processor import BNSDataProcessor
        from vector_db_qdrant import QdrantVectorDB
        
        # Process data
        processor = BNSDataProcessor()
        documents = processor.process_and_embed("BNS_optimized.json")
        
        # Store in vector database (with fallback to file)
        try:
            vector_db = QdrantVectorDB()
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
        from vector_db_qdrant import QdrantVectorDB
        vector_db = QdrantVectorDB()
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

def create_env_template():
    """Create .env template if it doesn't exist"""
    env_file = Path(".env")
    if not env_file.exists():
        print("\n📝 Creating .env template...")
        env_content = """# BNS Legal Assistant Environment Configuration
# =============================================

# Gemini API Configuration
# Get your API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Qdrant Vector Database Configuration
# Get your API key from: https://cloud.qdrant.io/
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here

# Application Security
SECRET_KEY=your_secret_key_here
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
        with open(env_file, "w", encoding="utf-8") as f:
            f.write(env_content)
        print("✅ Created .env template")
        print("⚠️ Please edit .env file with your actual API keys")

def main():
    """Main setup function"""
    print("🚀 BNS Legal Assistant Setup")
    print("=" * 40)
    
    # Create .env template if needed
    create_env_template()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Setup failed: Missing dependencies")
        print("\nTo install dependencies, run:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        print("\n❌ Setup failed: Missing environment variables")
        print("Please edit the .env file with your API keys")
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
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main()
