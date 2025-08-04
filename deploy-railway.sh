#!/bin/bash

echo "🚀 Deploying BNS Legal Assistant to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

# Login to Railway
echo "🔐 Logging into Railway..."
railway login

# Initialize project if not already done
if [ ! -f "railway.json" ]; then
    echo "📁 Initializing Railway project..."
    railway init
fi

# Set environment variables
echo "🔧 Setting environment variables..."
railway variables set GEMINI_API_KEY="$GEMINI_API_KEY"
railway variables set DATASTAX_API_KEY="$DATASTAX_API_KEY"
railway variables set DATASTAX_SECURE_CONNECT_BUNDLE_PATH="$DATASTAX_SECURE_CONNECT_BUNDLE_PATH"
railway variables set HOST="0.0.0.0"
railway variables set PORT="8000"

# Deploy
echo "🚀 Deploying to Railway..."
railway up

# Get the URL
echo "🌐 Getting deployment URL..."
railway domain

echo "✅ Deployment complete!"
echo "🎉 Your BNS Legal Assistant is now live!"
echo "📱 Access it at the URL above" 