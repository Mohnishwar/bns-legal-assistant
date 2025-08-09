from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import json
from dotenv import load_dotenv

# Import our custom modules
from data_processor import BNSDataProcessor
from vector_db_pinecone import PineconeVectorDB
from llm_interface import GeminiLLM

load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="BNS Legal Assistant API",
    description="AI-powered legal assistant for Bharatiya Nyaya Sanhita (BNS)",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Pydantic models
class QuestionRequest(BaseModel):
    question: str
    language: Optional[str] = "English"

class QuestionResponse(BaseModel):
    answer: str
    context_sections: List[str]
    model_used: str
    status: str
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    message: str
    services: Dict[str, str]

# Global instances
vector_db = None
llm = None
data_processor = None

def get_vector_db():
    global vector_db
    if vector_db is None:
        vector_db = PineconeVectorDB()
    return vector_db

def get_llm():
    global llm
    if llm is None:
        llm = GeminiLLM()
    return llm

def get_data_processor():
    global data_processor
    if data_processor is None:
        data_processor = BNSDataProcessor()
    return data_processor

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    try:
        # Test connections
        get_vector_db()
        get_llm()
        get_data_processor()
        print("✅ All services initialized successfully")
    except Exception as e:
        print(f"❌ Error during startup: {e}")

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "BNS Legal Assistant API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Test services
        vector_db = get_vector_db()
        llm = get_llm()
        
        services = {
            "vector_database": "✅ Connected",
            "llm": "✅ Connected",
            "data_processor": "✅ Ready"
        }
        
        return HealthResponse(
            status="healthy",
            message="All services are running",
            services=services
        )
        
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            message=f"Service error: {str(e)}",
            services={}
        )

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a legal question about BNS
    """
    try:
        vector_db = get_vector_db()
        llm = get_llm()
        
        # Get question embedding
        question_embedding = llm.get_embedding(request.question)
        
        # Search for relevant sections
        similar_docs = vector_db.search_similar(question_embedding, limit=3)
        
        if not similar_docs:
            return QuestionResponse(
                answer="I couldn't find relevant information in the BNS for your question. Please try rephrasing your question.",
                context_sections=[],
                model_used="gemini-1.5-flash",
                status="no_results"
            )
        
        # Prepare context
        context_sections = []
        for doc in similar_docs:
            section_info = f"Section {doc.get('section_number', 'N/A')}: {doc.get('section_title', 'N/A')}"
            context_sections.append(section_info)
        
        # Generate answer
        answer = llm.generate_response(request.question, similar_docs, request.language)
        
        return QuestionResponse(
            answer=answer,
            context_sections=context_sections,
            model_used="gemini-1.5-flash",
            status="success"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing question: {str(e)}"
        )

@app.post("/process-data")
async def process_bns_data():
    """
    Process BNS data and store in vector database
    """
    try:
        data_processor = get_data_processor()
        vector_db = get_vector_db()
        
        # Process and embed BNS data
        documents = data_processor.process_and_embed("BNS_optimized.json")
        
        # Store in vector database
        vector_db.insert_documents(documents)
        
        return {
            "message": "BNS data processed and stored successfully",
            "documents_processed": len(documents),
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing BNS data: {str(e)}"
        )

@app.get("/sections/{section_number}")
async def get_section(section_number: str):
    """
    Get a specific BNS section by number
    """
    try:
        vector_db = get_vector_db()
        
        # Search for sections with this number
        with open("bns_vector_data.json", "r", encoding="utf-8") as f:
            documents = json.load(f)
        
        matching_sections = [doc for doc in documents if doc.get('section_number') == section_number]
        
        if not matching_sections:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Section {section_number} not found"
            )
        
        return {
            "section_number": section_number,
            "sections": matching_sections
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving section: {str(e)}"
        )

@app.get("/chapters")
async def get_chapters():
    """
    Get list of all BNS chapters
    """
    try:
        with open("BNS_optimized.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        chapters = []
        for chapter in data.get('data', []):
            chapters.append({
                "chapter_number": chapter.get('chapter_number'),
                "chapter_title": chapter.get('chapter_title'),
                "section_count": len(chapter.get('sections', []))
            })
        
        return {"chapters": chapters}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving chapters: {str(e)}"
        )

# For Vercel serverless deployment
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
