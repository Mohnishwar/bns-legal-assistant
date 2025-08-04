#!/usr/bin/env python3
"""
DataStax API Token Helper
This script helps you get the correct DataStax API token
"""

def show_datastax_instructions():
    """Show step-by-step instructions for getting DataStax API token"""
    print("🔑 DataStax API Token Setup")
    print("=" * 40)
    print()
    print("Follow these steps to get your DataStax API token:")
    print()
    print("1. Go to https://astra.datastax.com/")
    print("2. Sign in to your account")
    print("3. Click on your database")
    print("4. Go to 'Settings' → 'API Keys'")
    print("5. Click 'Create API Key'")
    print("6. Give it a description (optional)")
    print("7. Set expiration to 'Never expire'")
    print("8. Click 'Generate token'")
    print("9. Copy the 'Client ID' (this is your API token)")
    print()
    print("⚠️  IMPORTANT: You need the 'Client ID', NOT the database URL!")
    print()
    print("❌ WRONG: https://08c510a2-4520-404f-89ef-1eedb61ba195-us-east-2.apps.astra.datastax.com")
    print("✅ RIGHT: AastraClientId_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    print()
    print("Your database ID is: 08c510a2-4520-404f-89ef-1eedb61ba195")
    print("This will be used to construct the database URL automatically.")
    print()
    
    # Ask if they want to proceed
    response = input("Do you have your Client ID ready? (y/N): ").lower()
    if response == 'y':
        client_id = input("Enter your DataStax Client ID: ").strip()
        if client_id and not client_id.startswith('http'):
            print(f"✅ Valid Client ID format: {client_id}")
            print("You can now run: python setup_env.py")
        else:
            print("❌ That looks like a URL, not a Client ID.")
            print("Please get the Client ID from the API Keys section.")
    else:
        print("Please get your Client ID first, then run this script again.")

if __name__ == "__main__":
    show_datastax_instructions() 