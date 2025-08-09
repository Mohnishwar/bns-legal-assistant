# BNS Legal Assistant

An AI-powered legal assistant for the Bharatiya Nyaya Sanhita (BNS) - India's new criminal code. This system helps common citizens understand legal concepts in simple language with contextual references to relevant legal sections.

## Features

- AI-Powered Legal Assistant: Uses Google Gemini 1.5 Flash for intelligent responses
- Vector Search: Advanced semantic search using Pinecone vector database
- Simple Language: Explains complex legal concepts in easy-to-understand terms
- Contextual References: Provides relevant BNS section numbers and citations
- Web Interface: User-friendly chat interface
- REST API: Full API for integration with other applications

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Google Gemini API key
- Pinecone API key (optional - system works with local file storage)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd BNS
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # The setup script will create a .env template
   python setup.py
   ```
   
   Then edit the `.env` file with your API keys:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   SECRET_KEY=your_secret_key_here
   HOST=0.0.0.0
   PORT=8000
   ```

4. **Run the setup**
   ```bash
   python setup.py
   ```

5. **Start the server**
   ```bash
   python main.py
   ```

6. **Access the web interface**
   Open your browser and go to: `http://localhost:8000/frontend/index.html`

## API Endpoints

### Health Check
```bash
GET /health
```

### Ask a Question
```bash
POST /ask
Content-Type: application/json

{
  "question": "What is the punishment for theft?",
  "language": "English"
}
```

### Process BNS Data
```bash
POST /process-data
```

### Get Chapters
```bash
GET /chapters
```

### Get Specific Section
```bash
GET /sections/{section_number}
```

## 📁 Project Structure

```
BNS/
├── main.py                 # FastAPI application
├── llm_interface.py        # Gemini LLM integration
├── data_processor.py       # BNS data processing
├── vector_db_pinecone.py   # Vector database interface
├── setup.py               # Setup script
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── BNS_optimized.json    # Main BNS data
├── BNS.json              # Original BNS data
├── BNS_optimized.csv     # CSV version
├── bns_vector_data.json  # Vector embeddings
└── frontend/
    └── index.html        # Web interface
```

## Getting API Keys

### Google Gemini API
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

### Pinecone API (Optional)
1. Go to [Pinecone Console](https://app.pinecone.io/)
2. Create a free account
3. Get your API key
4. Add it to your `.env` file

**Note**: If Pinecone is not available, the system will automatically use local file storage for vector search.

## 🛠️ Development

### Running in Development Mode
```bash
python main.py
```

### Testing the API
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test question endpoint
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the punishment for theft?"}'
```

## Deployment

### Local Deployment
The application is ready to run locally. Just follow the Quick Start instructions above.

### Cloud Deployment
This application can be deployed to various cloud platforms:

- **Railway**: Easy deployment with automatic environment variable management
- **Render**: Free tier available with automatic deployments
- **Heroku**: Traditional platform with good Python support
- **DigitalOcean App Platform**: Simple deployment with good performance

### Environment Variables for Production
```env
GEMINI_API_KEY=your_production_gemini_key
PINECONE_API_KEY=your_production_pinecone_key
SECRET_KEY=your_secure_secret_key
HOST=0.0.0.0
PORT=8000
DEBUG=False
```

## 📊 Data Sources

The system uses the Bharatiya Nyaya Sanhita (BNS) data, which includes:
- All chapters and sections
- Legal definitions and explanations
- Penalties and punishments
- Illustrations and examples
- Cross-references between sections

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is for educational and informational purposes. Please consult qualified legal professionals for specific legal advice.

## ⚠️ Disclaimer

This AI assistant provides general information about the BNS for educational purposes. It does not constitute legal advice. For specific legal matters, please consult qualified legal professionals.

## 🆘 Support

If you encounter any issues:

1. Check that all dependencies are installed
2. Verify your API keys are correct
3. Ensure the BNS data files are present
4. Check the logs for error messages

For more help, please open an issue on GitHub.

---

**Made with ❤️ for the Indian legal community**
