from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
import os
import json
from dotenv import load_dotenv

# Import our custom modules
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
llm = None

def get_llm():
    global llm
    if llm is None:
        llm = GeminiLLM()
    return llm

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    try:
        # Test connections
        get_llm()
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
    
    # Check LLM
    try:
        llm = get_llm()
        if llm.test_connection():
            services_status["llm"] = "healthy"
        else:
            services_status["llm"] = "unhealthy"
    except Exception as e:
        services_status["llm"] = f"unhealthy: {str(e)}"
    
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
        llm = get_llm()
        
        # For now, provide a simple response without vector search
        # This can be enhanced later with proper vector search
        response = llm.generate_simple_response(request.question)
        
        return QuestionResponse(
            answer=response,
            context_sections=["BNS Legal Assistant - AI Response"],
            model_used="gemini-1.5-flash",
            status="success"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing question: {str(e)}"
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
        "main_simple:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=False  # Disable reload in production
    ) 