from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
import os
from dotenv import load_dotenv

# Import our custom modules
from data_processor import BNSDataProcessor
from vector_db import DataStaxVectorDB
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

# Mount static files
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

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
        vector_db = DataStaxVectorDB()
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
    services_status = {}
    
    # Check vector database
    try:
        vector_db = get_vector_db()
        services_status["vector_db"] = "healthy"
    except Exception as e:
        services_status["vector_db"] = f"unhealthy: {str(e)}"
    
    # Check LLM
    try:
        llm = get_llm()
        if llm.test_connection():
            services_status["llm"] = "healthy"
        else:
            services_status["llm"] = "unhealthy"
    except Exception as e:
        services_status["llm"] = f"unhealthy: {str(e)}"
    
    # Check data processor
    try:
        data_processor = get_data_processor()
        services_status["data_processor"] = "healthy"
    except Exception as e:
        services_status["data_processor"] = f"unhealthy: {str(e)}"
    
    overall_status = "healthy" if all("healthy" in status for status in services_status.values()) else "unhealthy"
    
    return HealthResponse(
        status=overall_status,
        message="BNS Legal Assistant API Health Check",
        services=services_status
    )

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question about BNS and get an AI-generated response
    """
    try:
        # Get service instances
        vector_db = get_vector_db()
        llm = get_llm()
        data_processor = get_data_processor()
        
        # Generate embedding for the question
        question_embedding = data_processor.model.encode(request.question)
        
        # Search for relevant BNS sections
        relevant_docs = vector_db.search_similar(
            query_embedding=question_embedding.tolist(),
            limit=5
        )
        
        if not relevant_docs:
            return QuestionResponse(
                answer="I apologize, but I couldn't find relevant information in the BNS for your question. Please try rephrasing your question or ask about a different legal topic.",
                context_sections=[],
                model_used="gemini-flash-2.5",
                status="no_relevant_context"
            )
        
        # Generate response using LLM
        response = llm.generate_response(
            user_question=request.question,
            context_documents=relevant_docs
        )
        
        return QuestionResponse(**response)
        
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
        # This is a simplified search - you might want to implement a more sophisticated search
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

if __name__ == "__main__":
    import json
    
    # Run the server
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=False  # Disable reload in production
    ) 