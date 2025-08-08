import os
import json
from typing import List, Dict, Any, Optional
import pinecone
import numpy as np
from dotenv import load_dotenv

load_dotenv()

class PineconeVectorDB:
    def __init__(self):
        """
        Initialize Pinecone vector database
        """
        self.index_name = "bns-legal-assistant"
        self.dimension = 384  # Sentence transformers dimension
        self.connect()

    def connect(self):
        """
        Connect to Pinecone and initialize index
        """
        try:
            # Get API key from environment
            api_key = os.getenv('PINECONE_API_KEY')
            if not api_key:
                raise ValueError("PINECONE_API_KEY must be set in environment variables")

            # Initialize Pinecone
            pinecone.init(api_key=api_key, environment="us-east-1-aws")
            
            # Create index if it doesn't exist
            if self.index_name not in pinecone.list_indexes():
                pinecone.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric="cosine"
                )
                print(f"✅ Created Pinecone index: {self.index_name}")
            else:
                print(f"✅ Connected to existing Pinecone index: {self.index_name}")

            # Get index
            self.index = pinecone.Index(self.index_name)

        except Exception as e:
            print(f"❌ Error connecting to Pinecone: {e}")
            # Fallback to local file storage
            self.use_file_storage = True
            print("📁 Using local file storage as fallback")

    def insert_documents(self, documents: List[Dict[str, Any]]):
        """
        Insert documents into Pinecone
        """
        if hasattr(self, 'use_file_storage') and self.use_file_storage:
            return self.insert_to_file(documents)

        try:
            # Prepare vectors for Pinecone
            vectors = []
            for doc in documents:
                vector_id = doc['id']
                vector_values = doc['embedding']
                
                # Prepare metadata
                metadata = {
                    'chapter_number': doc.get('chapter_number', ''),
                    'chapter_title': doc.get('chapter_title', ''),
                    'section_number': doc.get('section_number', ''),
                    'section_title': doc.get('section_title', ''),
                    'content': doc.get('content', ''),
                    'full_text': doc.get('full_text', ''),
                    'status': doc.get('status', ''),
                    'jurisdiction': doc.get('jurisdiction', ''),
                    'keywords': ','.join(doc.get('keywords', [])),
                    'cross_references': ','.join(doc.get('cross_references', [])),
                    'penalties': ','.join(doc.get('penalties', [])),
                    'illustrations': ','.join(doc.get('illustrations', [])),
                    'chunk_index': doc.get('chunk_index', 0),
                    'total_chunks': doc.get('total_chunks', 1)
                }

                vectors.append({
                    'id': vector_id,
                    'values': vector_values,
                    'metadata': metadata
                })

            # Upsert vectors in batches
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                self.index.upsert(vectors=batch)

            print(f"✅ Inserted {len(documents)} documents into Pinecone")

        except Exception as e:
            print(f"❌ Error inserting into Pinecone: {e}")
            # Fallback to file storage
            self.insert_to_file(documents)

    def insert_to_file(self, documents: List[Dict[str, Any]]):
        """
        Fallback: Store documents in local file
        """
        try:
            with open("bns_vector_data.json", "w", encoding="utf-8") as f:
                json.dump(documents, f, indent=2, ensure_ascii=False)
            print(f"✅ Stored {len(documents)} documents in local file")
        except Exception as e:
            print(f"❌ Error storing in file: {e}")

    def search_similar(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar documents using Pinecone
        """
        if hasattr(self, 'use_file_storage') and self.use_file_storage:
            return self.search_in_file(query_embedding, limit)

        try:
            # Query Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=limit,
                include_metadata=True
            )

            # Convert results to our format
            documents = []
            for match in results.matches:
                metadata = match.metadata
                doc = {
                    'id': match.id,
                    'chapter_number': metadata.get('chapter_number', ''),
                    'chapter_title': metadata.get('chapter_title', ''),
                    'section_number': metadata.get('section_number', ''),
                    'section_title': metadata.get('section_title', ''),
                    'content': metadata.get('content', ''),
                    'full_text': metadata.get('full_text', ''),
                    'status': metadata.get('status', ''),
                    'jurisdiction': metadata.get('jurisdiction', ''),
                    'keywords': metadata.get('keywords', '').split(',') if metadata.get('keywords') else [],
                    'cross_references': metadata.get('cross_references', '').split(',') if metadata.get('cross_references') else [],
                    'penalties': metadata.get('penalties', '').split(',') if metadata.get('penalties') else [],
                    'illustrations': metadata.get('illustrations', '').split(',') if metadata.get('illustrations') else [],
                    'chunk_index': metadata.get('chunk_index', 0),
                    'total_chunks': metadata.get('total_chunks', 1),
                    'score': match.score
                }
                documents.append(doc)

            return documents

        except Exception as e:
            print(f"❌ Error searching in Pinecone: {e}")
            return self.search_in_file(query_embedding, limit)

    def search_in_file(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Fallback: Search in local file using cosine similarity
        """
        try:
            with open("bns_vector_data.json", "r", encoding="utf-8") as f:
                documents = json.load(f)

            # Calculate cosine similarity
            similarities = []
            query_embedding = np.array(query_embedding)

            for doc in documents:
                doc_embedding = np.array(doc['embedding'])
                similarity = np.dot(query_embedding, doc_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
                )
                similarities.append((similarity, doc))

            # Sort by similarity and return top results
            similarities.sort(key=lambda x: x[0], reverse=True)
            return [doc for _, doc in similarities[:limit]]

        except Exception as e:
            print(f"❌ Error searching in file: {e}")
            return []

    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific document by ID
        """
        if hasattr(self, 'use_file_storage') and self.use_file_storage:
            return self.get_document_from_file(doc_id)

        try:
            # Query Pinecone for specific ID
            results = self.index.query(
                vector=[0.0] * self.dimension,  # Dummy vector
                top_k=1,
                filter={"id": doc_id},
                include_metadata=True
            )

            if results.matches:
                match = results.matches[0]
                metadata = match.metadata
                return {
                    'id': match.id,
                    'chapter_number': metadata.get('chapter_number', ''),
                    'chapter_title': metadata.get('chapter_title', ''),
                    'section_number': metadata.get('section_number', ''),
                    'section_title': metadata.get('section_title', ''),
                    'content': metadata.get('content', ''),
                    'full_text': metadata.get('full_text', ''),
                    'status': metadata.get('status', ''),
                    'jurisdiction': metadata.get('jurisdiction', ''),
                    'keywords': metadata.get('keywords', '').split(',') if metadata.get('keywords') else [],
                    'cross_references': metadata.get('cross_references', '').split(',') if metadata.get('cross_references') else [],
                    'penalties': metadata.get('penalties', '').split(',') if metadata.get('penalties') else [],
                    'illustrations': metadata.get('illustrations', '').split(',') if metadata.get('illustrations') else [],
                    'chunk_index': metadata.get('chunk_index', 0),
                    'total_chunks': metadata.get('total_chunks', 1),
                    'score': match.score
                }
            return None

        except Exception as e:
            print(f"❌ Error retrieving document: {e}")
            return self.get_document_from_file(doc_id)

    def get_document_from_file(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Fallback: Get document from local file
        """
        try:
            with open("bns_vector_data.json", "r", encoding="utf-8") as f:
                documents = json.load(f)

            for doc in documents:
                if doc['id'] == doc_id:
                    return doc
            return None

        except Exception as e:
            print(f"❌ Error retrieving from file: {e}")
            return None

    def close(self):
        """
        Close the database connection
        """
        # Pinecone doesn't require explicit connection closing
        pass
