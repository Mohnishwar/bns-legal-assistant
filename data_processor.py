import json
import uuid
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import numpy as np

class BNSDataProcessor:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the BNS data processor with a sentence transformer model
        """
        self.model = SentenceTransformer(model_name)
        
    def load_bns_data(self, file_path: str) -> Dict[str, Any]:
        """
        Load BNS data from JSON file
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def chunk_text(self, text: str, max_length: int = 512) -> List[str]:
        """
        Split text into chunks for better vector search
        """
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk + sentence) < max_length:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks
    
    def process_section(self, section: Dict[str, Any], chapter_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process a single BNS section into vector-ready documents
        """
        documents = []
        
        # Create main section document
        section_text = " ".join(section.get('text', []))
        section_chunks = self.chunk_text(section_text)
        
        for i, chunk in enumerate(section_chunks):
            doc = {
                'id': str(uuid.uuid4()),
                'type': 'section',
                'chapter_number': chapter_info.get('chapter_number', ''),
                'chapter_title': chapter_info.get('chapter_title', ''),
                'section_number': section.get('section_number', ''),
                'section_title': section.get('section_title', ''),
                'content': chunk,
                'full_text': section_text,
                'status': section.get('status', 'Active'),
                'jurisdiction': section.get('jurisdiction', 'India'),
                'keywords': section.get('keywords', []),
                'cross_references': section.get('cross_references', []),
                'penalties': section.get('penalties', []),
                'illustrations': section.get('illustrations', []),
                'chunk_index': i,
                'total_chunks': len(section_chunks)
            }
            documents.append(doc)
        
        return documents
    
    def process_bns_data(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process entire BNS data into vector-ready documents
        """
        all_documents = []
        
        for chapter in data.get('data', []):
            chapter_info = {
                'chapter_number': chapter.get('chapter_number', ''),
                'chapter_title': chapter.get('chapter_title', ''),
                'preamble_text': chapter.get('preamble_text', '')
            }
            
            # Process each section in the chapter
            for section in chapter.get('sections', []):
                section_docs = self.process_section(section, chapter_info)
                all_documents.extend(section_docs)
        
        return all_documents
    
    def generate_embeddings(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate embeddings for all documents
        """
        texts = [doc['content'] for doc in documents]
        embeddings = self.model.encode(texts)
        
        for i, doc in enumerate(documents):
            doc['embedding'] = embeddings[i].tolist()
        
        return documents
    
    def process_and_embed(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Complete pipeline: load, process, and embed BNS data
        """
        print("Loading BNS data...")
        data = self.load_bns_data(file_path)
        
        print("Processing sections...")
        documents = self.process_bns_data(data)
        
        print(f"Generated {len(documents)} document chunks")
        
        print("Generating embeddings...")
        documents_with_embeddings = self.generate_embeddings(documents)
        
        print("Processing complete!")
        return documents_with_embeddings

if __name__ == "__main__":
    processor = BNSDataProcessor()
    documents = processor.process_and_embed("BNS_optimized.json")
    
    # Save processed data
    with open("bns_processed.json", "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)
    
    print(f"Processed data saved to bns_processed.json")
    print(f"Total documents: {len(documents)}") 