# BNS Legal Assistant 🏛️

A comprehensive AI-powered legal assistant for the Bharatiya Nyaya Sanhita (BNS) - India's new criminal code. This system provides legal information, answers queries, and helps users understand criminal law provisions.

## 🌟 Features

- **AI-Powered Legal Queries**: Get answers to legal questions using Gemini 1.5 Flash
- **Comprehensive BNS Coverage**: Access to all sections of the Bharatiya Nyaya Sanhita
- **Vector Database Search**: Fast and accurate retrieval of relevant legal information
- **RESTful API**: Easy integration with web applications and mobile apps
- **Web Interface**: User-friendly frontend for legal queries

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Git
- Internet connection for API access

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd BNS
   ```

2. **Create a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your API keys
   GEMINI_API_KEY=your_gemini_api_key_here
   QDRANT_URL=your_qdrant_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   ```

5. **Run the system**
   ```bash
   python main.py
   ```

6. **Access the system**
   - API: http://localhost:8001
   - Web Interface: http://localhost:8001/frontend/index.html
   - Health Check: http://localhost:8001/health

## 🔑 API Keys Setup

### 1. Gemini API Key
- Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- Create a new API key
- Add it to your `.env` file

### 2. Qdrant Vector Database
- Visit [Qdrant Cloud](https://cloud.qdrant.io/)
- Create a new cluster
- Get your URL and API key
- Add them to your `.env` file

## 📁 Project Structure

```
BNS/
├── main.py                 # Main FastAPI application
├── llm_interface.py        # Gemini LLM integration
├── vector_db_qdrant.py     # Qdrant vector database operations
├── data_processor.py       # BNS data processing and embedding
├── setup.py               # System setup and initialization
├── requirements.txt        # Python dependencies
├── .env                   # Environment configuration
├── BNS_optimized.json     # Core BNS dataset
├── frontend/              # Web interface
│   └── index.html         # Main web page
└── README.md              # This file
```

## 🛠️ API Endpoints

### Core Endpoints

- **`GET /health`** - System health check
- **`POST /ask`** - Ask legal questions
- **`GET /chapters`** - List all BNS chapters
- **`GET /sections/{section_number}`** - Get specific section details
- **`POST /process-data`** - Reprocess BNS data

### Example API Usage

```bash
# Ask a legal question
curl -X POST "http://localhost:8001/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the penalty for theft?", "language": "English"}'

# Check system health
curl "http://localhost:8001/health"

# Get all chapters
curl "http://localhost:8001/chapters"
```

## 🧪 Testing the System

After starting the system, you can test it with various legal questions:

- "What is the penalty for theft?"
- "What is the punishment for murder?"
- "What is the penalty for causing hurt?"
- "What is the punishment for cheating?"
- "What is the Bharatiya Nyaya Sanhita?"

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `QDRANT_URL` | Qdrant vector database URL | Yes |
| `QDRANT_API_KEY` | Qdrant API key | Yes |
| `HOST` | Server host (default: 0.0.0.0) | No |
| `PORT` | Server port (default: 8000) | No |

### Port Configuration

If port 8000 is busy, you can change it:

```bash
# Set environment variable
export PORT=8001  # Linux/macOS
set PORT=8001     # Windows

# Or modify .env file
PORT=8001
```

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Production Deployment
```bash
# Install production dependencies
pip install -r requirements.txt

# Set production environment
export ENV=production

# Run with uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
```

## 📊 System Performance

The system has been tested with 50 comprehensive test cases and shows:
- **Overall Accuracy**: 60.0%
- **Response Time**: ~5.1 seconds average
- **Coverage**: Excellent for core criminal offenses, good for specialized areas

### Performance by Category
- **Core Crimes** (theft, assault, murder): 100% accuracy
- **Property Crimes**: 100% accuracy
- **Sexual Offenses**: 100% accuracy
- **Cybercrime**: 20% accuracy (needs improvement)
- **Specialized Crimes**: Variable performance

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Change port in .env file
   PORT=8001
   ```

2. **API Key Errors**
   - Verify your API keys in `.env` file
   - Check if keys have proper permissions

3. **Vector Database Connection Issues**
   - Verify Qdrant URL and API key
   - Check internet connectivity

4. **Memory Issues**
   - Ensure sufficient RAM (recommended: 4GB+)
   - Close other applications

### Logs

Check the console output for detailed error messages and system status.

**Note**: This system is for educational and informational purposes. For legal advice, always consult qualified legal professionals.
