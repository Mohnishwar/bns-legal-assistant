# 🤖 BNS Legal Assistant

An AI-powered legal assistant for the **Bharatiya Nyaya Sanhita (BNS)** - India's new criminal code. This intelligent system helps common citizens understand complex legal concepts in simple language with contextual references to relevant legal sections.

## 🌟 Features

- **🤖 AI-Powered Responses**: Powered by Google Gemini 1.5 Flash
- **🔍 Vector Search**: Intelligent retrieval of relevant BNS sections
- **🌐 Web Interface**: Modern, user-friendly chat interface
- **📚 Comprehensive Coverage**: All 358 BNS sections processed and indexed
- **🔗 Contextual References**: Direct links to relevant legal sections
- **⚡ Real-time Processing**: Instant responses to legal queries

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Google Gemini API Key
- DataStax Astra DB (optional - local storage fallback available)

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd BNS
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv311
   source venv311/bin/activate  # On Windows: venv311\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run setup:**
   ```bash
   python setup.py
   ```

6. **Start the server:**
   ```bash
   python main.py
   ```

7. **Access the application:**
   ```
   http://localhost:8000/frontend/index.html
   ```

## 🌐 Online Deployment

### Railway (Recommended)
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

### Other Options
- **Render**: Connect GitHub repo and deploy
- **Heroku**: Use Heroku CLI
- **DigitalOcean**: App Platform deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 📁 Project Structure

```
BNS/
├── main.py                 # FastAPI application
├── data_processor.py       # BNS data processing
├── vector_db.py           # Vector database interface
├── llm_interface.py       # Gemini LLM interface
├── frontend/
│   └── index.html         # Web interface
├── BNS_optimized.json     # BNS legal data
├── bns_vector_data.json   # Processed embeddings
├── requirements.txt        # Dependencies
├── setup.py              # Setup script
└── DEPLOYMENT.md         # Deployment guide
```

## 🔧 API Endpoints

- `GET /` - API root
- `GET /health` - Health check
- `POST /ask` - Ask legal questions
- `GET /chapters` - List BNS chapters
- `GET /sections/{number}` - Get specific section
- `POST /process-data` - Reprocess BNS data

## 🎯 Usage Examples

### Ask Legal Questions
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the punishment for theft?"}'
```

### Health Check
```bash
curl http://localhost:8000/health
```

## 🔑 Environment Variables

```bash
GEMINI_API_KEY=your_gemini_api_key
DATASTAX_API_KEY=your_datastax_api_key
DATASTAX_SECURE_CONNECT_BUNDLE_PATH=path_to_bundle
HOST=0.0.0.0
PORT=8000
```

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **AI/LLM**: Google Gemini 1.5 Flash
- **Vector Database**: DataStax Astra DB (with local fallback)
- **Embeddings**: Sentence Transformers
- **Frontend**: HTML/JavaScript
- **Deployment**: Railway/Render/Heroku

## 📊 System Status

- ✅ **358 BNS sections** processed and embedded
- ✅ **Vector search** working
- ✅ **AI responses** functional
- ✅ **Web interface** accessible
- ✅ **API endpoints** operational

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google Gemini** for AI capabilities
- **DataStax Astra** for vector database
- **FastAPI** for the web framework
- **Indian Legal System** for the BNS data

## 📞 Support

For issues or questions:
1. Check the [DEPLOYMENT.md](DEPLOYMENT.md) guide
2. Verify environment variables
3. Test the health endpoint
4. Check deployment logs

---

**🎉 Your AI-powered BNS Legal Assistant is ready to help citizens understand India's new criminal code!** 
