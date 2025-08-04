# 🚀 BNS Legal Assistant - Deployment Guide

## 📋 Prerequisites

Before deploying, ensure you have:
- ✅ All API keys configured in `.env`
- ✅ Python 3.11 environment
- ✅ All dependencies installed
- ✅ System tested locally

## 🌐 Deployment Options

### Option 1: Railway (Recommended - Easiest)

**Railway** is perfect for Python FastAPI apps with automatic deployments.

#### Steps:
1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Initialize Railway project:**
   ```bash
   railway init
   ```

4. **Set environment variables:**
   ```bash
   railway variables set GEMINI_API_KEY=your_gemini_key
   railway variables set DATASTAX_API_KEY=your_datastax_key
   railway variables set DATASTAX_SECURE_CONNECT_BUNDLE_PATH=your_bundle_path
   ```

5. **Deploy:**
   ```bash
   railway up
   ```

6. **Get your URL:**
   ```bash
   railway domain
   ```

### Option 2: Render

**Render** offers free hosting for web services.

#### Steps:
1. **Create account** at [render.com](https://render.com)
2. **Connect your GitHub repository**
3. **Create a new Web Service**
4. **Configure:**
   - **Build Command:** `pip install -r requirements-prod.txt`
   - **Start Command:** `python main.py`
   - **Environment Variables:** Add all from `.env`

### Option 3: Heroku

**Heroku** is a classic choice for Python apps.

#### Steps:
1. **Install Heroku CLI:**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login:**
   ```bash
   heroku login
   ```

3. **Create app:**
   ```bash
   heroku create your-bns-app-name
   ```

4. **Set environment variables:**
   ```bash
   heroku config:set GEMINI_API_KEY=your_gemini_key
   heroku config:set DATASTAX_API_KEY=your_datastax_key
   heroku config:set DATASTAX_SECURE_CONNECT_BUNDLE_PATH=your_bundle_path
   ```

5. **Deploy:**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### Option 4: DigitalOcean App Platform

**DigitalOcean** offers reliable cloud hosting.

#### Steps:
1. **Create account** at [digitalocean.com](https://digitalocean.com)
2. **Go to App Platform**
3. **Connect your GitHub repository**
4. **Configure the app:**
   - **Source:** Your GitHub repo
   - **Branch:** main
   - **Build Command:** `pip install -r requirements-prod.txt`
   - **Run Command:** `python main.py`
   - **Environment Variables:** Add all from `.env`

## 🔧 Environment Variables Setup

For any deployment, you need these environment variables:

```bash
GEMINI_API_KEY=your_gemini_api_key
DATASTAX_API_KEY=your_datastax_api_key
DATASTAX_SECURE_CONNECT_BUNDLE_PATH=path_to_secure_bundle
HOST=0.0.0.0
PORT=8000
```

## 📁 Files for Deployment

Ensure these files are in your repository:
- ✅ `main.py` - FastAPI application
- ✅ `requirements-prod.txt` - Production dependencies
- ✅ `railway.json` - Railway configuration
- ✅ `Procfile` - Process file
- ✅ `runtime.txt` - Python version
- ✅ `frontend/index.html` - Web interface
- ✅ `BNS_optimized.json` - BNS data
- ✅ `bns_vector_data.json` - Processed embeddings

## 🚀 Quick Deploy Commands

### Railway (Fastest):
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

### Render:
1. Push to GitHub
2. Connect to Render
3. Deploy automatically

## 🔍 Post-Deployment Checklist

After deployment, verify:
- ✅ **Health Check:** `https://your-app.railway.app/health`
- ✅ **API Root:** `https://your-app.railway.app/`
- ✅ **Frontend:** `https://your-app.railway.app/frontend/index.html`
- ✅ **Ask Question:** Test the `/ask` endpoint

## 🛠️ Troubleshooting

### Common Issues:

1. **Port Issues:**
   - Ensure `HOST=0.0.0.0` and `PORT=8000`

2. **Environment Variables:**
   - Double-check all API keys are set correctly

3. **Dependencies:**
   - Use `requirements-prod.txt` for production

4. **Data Files:**
   - Ensure `BNS_optimized.json` and `bns_vector_data.json` are included

## 🌟 Recommended: Railway Deployment

**Railway** is recommended because:
- ✅ **Free tier** with generous limits
- ✅ **Automatic deployments** from GitHub
- ✅ **Easy environment variable management**
- ✅ **Built-in monitoring**
- ✅ **Fast setup** (5 minutes)

## 📞 Support

If you encounter issues:
1. Check the deployment logs
2. Verify environment variables
3. Test locally first
4. Check the health endpoint

---

**Your BNS Legal Assistant will be live at:** `https://your-app-name.railway.app` 