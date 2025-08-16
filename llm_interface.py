import os
import google.generativeai as genai
from typing import List, Dict, Any, Optional

# Load environment variables from .env file
# API key should be set in .env file, not hardcoded here

class GeminiLLM:
    def __init__(self):
        """
        Initialize Gemini 1.5 Flash LLM interface
        """
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        genai.configure(api_key=self.api_key)

        # Initialize the model
        try:
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            print("✅ Connected to Gemini 1.5 Flash")
        except Exception as e:
            print(f"❌ Error connecting to Gemini: {e}")
            raise

    def generate_response(self,
                         user_question: str,
                         context_documents: List[Dict[str, Any]],
                         system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a response using Gemini 1.5 Flash with context from BNS sections
        """
        try:
            # Prepare context from relevant BNS sections
            context_text = self._prepare_context(context_documents)

            # Create the prompt
            if system_prompt is None:
                system_prompt = self._get_default_system_prompt()

            full_prompt = f"""
{system_prompt}

**Relevant BNS Sections:**
{context_text}

**User Question:** {user_question}

Please provide a clear, accurate, and helpful response based on the Bharatiya Nyaya Sanhita (BNS) sections provided above. Include relevant section numbers and references where applicable.
"""

            # Generate response
            response = self.model.generate_content(full_prompt)

            return {
                'answer': response.text,
                'context_sections': [doc['section_number'] for doc in context_documents],
                'model_used': 'gemini-1.5-flash',
                'status': 'success'
            }

        except Exception as e:
            print(f"❌ Error generating response: {e}")
            return {
                'answer': f"I apologize, but I encountered an error while processing your question. Please try again or rephrase your question.",
                'context_sections': [],
                'model_used': 'gemini-1.5-flash',
                'status': 'error',
                'error': str(e)
            }

    def _prepare_context(self, documents: List[Dict[str, Any]]) -> str:
        """
        Prepare context text from relevant BNS documents
        """
        context_parts = []

        for doc in documents:
            section_info = f"**Section {doc.get('section_number', 'N/A')} - {doc.get('section_title', 'N/A')}**"
            section_info += f"\nChapter: {doc.get('chapter_number', 'N/A')} - {doc.get('chapter_title', 'N/A')}"
            section_info += f"\nContent: {doc.get('content', '')}"

            if doc.get('illustrations'):
                section_info += f"\nIllustrations: {'; '.join(doc['illustrations'])}"

            if doc.get('penalties'):
                section_info += f"\nPenalties: {'; '.join(doc['penalties'])}"

            context_parts.append(section_info)

        return "\n\n".join(context_parts)

    def _get_default_system_prompt(self) -> str:
        """
        Get the default system prompt for BNS legal assistant
        """
        return """You are an AI-powered legal assistant for the Bharatiya Nyaya Sanhita (BNS), India's new criminal code. Your role is to help common citizens understand legal concepts in simple, clear language.

**Your Responsibilities:**
1. Provide accurate information based on the BNS sections provided
2. Explain legal concepts in simple, understandable language
3. Always cite relevant section numbers when referencing the law
4. Clarify that you are providing general information and not legal advice
5. Encourage users to consult qualified legal professionals for specific legal matters

**Guidelines:**
- Use clear, simple language that non-lawyers can understand
- Always reference specific BNS sections when providing information
- If a question is outside the scope of the provided context, say so clearly
- Be helpful but remind users that this is for informational purposes only
- If you're unsure about something, say so rather than guessing

**Important:** This system provides general information about the BNS for educational purposes. It does not constitute legal advice. For specific legal matters, users should consult qualified legal professionals."""

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using Gemini's embedding model
        """
        try:
            # Note: This is a placeholder. You'll need to use the appropriate
            # embedding model from Google's API
            # For now, we'll use a simple approach
            embedding_model = genai.get_embedding_model('embedding-001')
            result = embedding_model.embed_content(text)
            return result['embedding']
        except Exception as e:
            print(f"❌ Error generating embedding: {e}")
            # Return a dummy embedding for fallback
            return [0.0] * 384  # Standard embedding size

    def test_connection(self) -> bool:
        """
        Test the connection to Gemini API
        """
        try:
            test_prompt = "Hello, this is a test message."
            response = self.model.generate_content(test_prompt)
            return response.text is not None
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False
    
    def generate_simple_response(self, question: str) -> str:
        """Generate a simple response without vector search"""
        try:
            prompt = f"""
            You are an AI Legal Assistant for the Bharatiya Nyaya Sanhita (BNS) - India's new criminal code.
            
            Question: {question}
            
            Please provide a helpful, accurate response about BNS. If you don't have specific information about the question, 
            provide general guidance about BNS and suggest consulting a legal professional for specific legal advice.
            
            Keep your response clear, informative, and helpful for common citizens.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"I apologize, but I encountered an error while processing your question. Please try again or contact support. Error: {str(e)}"

if __name__ == "__main__":
    # Test the LLM interface
    try:
        llm = GeminiLLM()
        if llm.test_connection():
            print("✅ Gemini LLM connection successful!")
        else:
            print("❌ Gemini LLM connection failed!")
    except Exception as e:
        print(f"❌ Error initializing Gemini LLM: {e}") 