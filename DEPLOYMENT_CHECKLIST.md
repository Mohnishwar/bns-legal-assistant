# ✅ Deployment Checklist

## 📋 Pre-Deployment Checklist

### ✅ Environment Setup
- [ ] Python 3.11 environment created
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Virtual environment activated
- [ ] Local system tested and working

### ✅ API Keys & Configuration
- [ ] Google Gemini API key obtained and configured
- [ ] DataStax API key obtained (optional - local fallback works)
- [ ] DataStax secure connect bundle downloaded (optional)
- [ ] `.env` file created with all required variables

### ✅ Data Processing
- [ ] BNS data processed (`python setup.py`)
- [ ] 745 sections embedded successfully
- [ ] `bns_vector_data.json` created
- [ ] Health check passes (`/health` endpoint)

### ✅ Local Testing
- [ ] Server starts without errors
- [ ] Web interface accessible at `http://localhost:8000/frontend/index.html`
- [ ] API endpoints responding correctly
- [ ] Can ask questions and get responses
- [ ] Vector search working

## 🚀 Deployment Options

### Option 1: Railway (Recommended)
- [ ] Install Railway CLI: `npm install -g @railway/cli`
- [ ] Login to Railway: `railway login`
- [ ] Initialize project: `railway init`
- [ ] Set environment variables
- [ ] Deploy: `railway up`
- [ ] Get URL: `railway domain`

### Option 2: Render
- [ ] Create Render account
- [ ] Connect GitHub repository
- [ ] Create new Web Service
- [ ] Configure build and start commands
- [ ] Set environment variables
- [ ] Deploy

### Option 3: Heroku
- [ ] Install Heroku CLI
- [ ] Login: `heroku login`
- [ ] Create app: `heroku create your-app-name`
- [ ] Set config vars
- [ ] Deploy: `git push heroku main`

## 📁 Required Files for Deployment

### ✅ Core Application Files
- [ ] `main.py` - FastAPI application
- [ ] `data_processor.py` - Data processing
- [ ] `vector_db.py` - Vector database interface
- [ ] `llm_interface.py` - LLM interface
- [ ] `setup.py` - Setup script

### ✅ Configuration Files
- [ ] `requirements-prod.txt` - Production dependencies
- [ ] `railway.json` - Railway configuration
- [ ] `Procfile` - Process file
- [ ] `runtime.txt` - Python version

### ✅ Data Files
- [ ] `BNS_optimized.json` - BNS legal data
- [ ] `bns_vector_data.json` - Processed embeddings
- [ ] `frontend/index.html` - Web interface

### ✅ Documentation
- [ ] `README.md` - Project documentation
- [ ] `DEPLOYMENT.md` - Deployment guide
- [ ] `DEPLOYMENT_CHECKLIST.md` - This checklist

## 🔧 Environment Variables for Deployment

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key
HOST=0.0.0.0
PORT=8000

# Optional (for DataStax)
DATASTAX_API_KEY=your_datastax_api_key
DATASTAX_SECURE_CONNECT_BUNDLE_PATH=path_to_bundle
```

## 🧪 Post-Deployment Testing

### ✅ Health Checks
- [ ] Health endpoint: `https://your-app.railway.app/health`
- [ ] API root: `https://your-app.railway.app/`
- [ ] Frontend: `https://your-app.railway.app/frontend/index.html`

### ✅ Functionality Tests
- [ ] Can ask questions via web interface
- [ ] API responds to POST `/ask` requests
- [ ] Vector search returns relevant results
- [ ] AI generates appropriate responses
- [ ] Error handling works correctly

### ✅ Performance Tests
- [ ] Response time under 5 seconds
- [ ] Can handle multiple concurrent requests
- [ ] Memory usage is reasonable
- [ ] No memory leaks

## 🛠️ Troubleshooting

### Common Issues:
1. **Environment Variables Not Set**
   - Check deployment platform's environment variable settings
   - Verify all required variables are configured

2. **Port Issues**
   - Ensure `HOST=0.0.0.0` and `PORT=8000`
   - Some platforms use `PORT` environment variable

3. **Dependencies Issues**
   - Use `requirements-prod.txt` for production
   - Check Python version compatibility

4. **Data Files Missing**
   - Ensure `BNS_optimized.json` and `bns_vector_data.json` are included
   - Check file paths in deployment

## 🎉 Success Criteria

Your deployment is successful when:
- ✅ Application is accessible via HTTPS URL
- ✅ Health check returns "healthy" status
- ✅ Can ask questions and get AI responses
- ✅ Web interface loads and functions correctly
- ✅ API endpoints respond as expected
- ✅ No critical errors in deployment logs

---

**🚀 Ready to deploy! Choose your preferred platform and follow the deployment guide.** 