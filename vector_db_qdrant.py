import os
import json
from typing import List, Dict, Any, Optional
import requests
import numpy as np
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set environment variables directly to avoid .env file encoding issues
if not os.getenv('QDRANT_URL'):
    os.environ['QDRANT_URL'] = 'https://2a10e5da-88cf-4479-98a1-e1d7bd5dba3f.eu-west-1-0.aws.cloud.qdrant.io'
if not os.getenv('QDRANT_API_KEY'):
    os.environ['QDRANT_API_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.8gGfThk4PVjSEGgNWouRtkwyhN3yl-aYDdGkuN2mlio'

class QdrantVectorDB:
    def __init__(self):
        """
        Initialize Qdrant vector database
        """
        self.collection_name = "bns_legal_assistant"
        self.dimension = 384  # Sentence transformers dimension
        self.url = os.getenv('QDRANT_URL', 'https://your-cluster.qdrant.io')
        self.api_key = os.getenv('QDRANT_API_KEY')
        self.connect()

    def connect(self):
        """
        Connect to Qdrant and initialize collection
        """
        try:
            if not self.api_key:
                print("⚠️ QDRANT_API_KEY not set, using local file storage")
                self.use_file_storage = True
                return

            headers = {"api-key": self.api_key}
            
            # Check if collection exists
            response = requests.get(
                f"{self.url}/collections/{self.collection_name}",
                headers=headers
            )
            
            if response.status_code == 404:
                # Create collection
                create_payload = {
                    "vectors": {
                        "size": self.dimension,
                        "distance": "Cosine"
                    }
                }
                
                response = requests.put(
                    f"{self.url}/collections/{self.collection_name}",
                    headers=headers,
                    json=create_payload
                )
                
                if response.status_code == 200:
                    print(f"✅ Created Qdrant collection: {self.collection_name}")
                else:
                    raise Exception(f"Failed to create collection: {response.text}")
            else:
                print(f"✅ Connected to existing Qdrant collection: {self.collection_name}")

        except Exception as e:
            print(f"❌ Error connecting to Qdrant: {e}")
            self.use_file_storage = True
            print("📁 Using local file storage as fallback")

    def insert_documents(self, documents: List[Dict[str, Any]]):
        """
        Insert documents into Qdrant
        """
        if hasattr(self, 'use_file_storage') and self.use_file_storage:
            return self.insert_to_file(documents)

        try:
            headers = {"api-key": self.api_key}
            
            # Prepare points for Qdrant
            points = []
            for doc in documents:
                point = {
                    "id": doc['id'],
                    "vector": doc['embedding'],
                    "payload": {
                        'chapter_number': doc.get('chapter_number', ''),
                        'chapter_title': doc.get('chapter_title', ''),
                        'section_number': doc.get('section_number', ''),
                        'section_title': doc.get('section_title', ''),
                        'content': doc.get('content', ''),
                        'full_text': doc.get('full_text', ''),
                        'status': doc.get('status', ''),
                        'jurisdiction': doc.get('jurisdiction', ''),
                        'keywords': doc.get('keywords', []),
                        'cross_references': doc.get('cross_references', []),
                        'penalties': doc.get('penalties', []),
                        'illustrations': doc.get('illustrations', []),
                        'chunk_index': doc.get('chunk_index', 0),
                        'total_chunks': doc.get('total_chunks', 1)
                    }
                }
                points.append(point)

            # Insert in batches
            batch_size = 100
            for i in range(0, len(points), batch_size):
                batch = points[i:i + batch_size]
                
                response = requests.put(
                    f"{self.url}/collections/{self.collection_name}/points",
                    headers=headers,
                    json={"points": batch}
                )
                
                if response.status_code != 200:
                    raise Exception(f"Failed to insert batch: {response.text}")

            print(f"✅ Inserted {len(documents)} documents into Qdrant")

        except Exception as e:
            print(f"❌ Error inserting into Qdrant: {e}")
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
        Search for similar documents using Qdrant
        """
        if hasattr(self, 'use_file_storage') and self.use_file_storage:
            return self.search_in_file(query_embedding, limit)

        try:
            headers = {"api-key": self.api_key}
            
            search_payload = {
                "vector": query_embedding,
                "limit": limit,
                "with_payload": True
            }
            
            response = requests.post(
                f"{self.url}/collections/{self.collection_name}/points/search",
                headers=headers,
                json=search_payload
            )
            
            if response.status_code != 200:
                raise Exception(f"Search failed: {response.text}")
            
            results = response.json()
            
            # Convert results to our format
            documents = []
            for result in results.get('result', []):
                payload = result.get('payload', {})
                doc = {
                    'id': result.get('id'),
                    'chapter_number': payload.get('chapter_number', ''),
                    'chapter_title': payload.get('chapter_title', ''),
                    'section_number': payload.get('section_number', ''),
                    'section_title': payload.get('section_title', ''),
                    'content': payload.get('content', ''),
                    'full_text': payload.get('full_text', ''),
                    'status': payload.get('status', ''),
                    'jurisdiction': payload.get('jurisdiction', ''),
                    'keywords': payload.get('keywords', []),
                    'cross_references': payload.get('cross_references', []),
                    'penalties': payload.get('penalties', []),
                    'illustrations': payload.get('illustrations', []),
                    'chunk_index': payload.get('chunk_index', 0),
                    'total_chunks': payload.get('total_chunks', 1),
                    'score': result.get('score', 0)
                }
                documents.append(doc)

            return documents

        except Exception as e:
            print(f"❌ Error searching in Qdrant: {e}")
            return self.search_in_file(query_embedding, limit)

    def search_in_file(self, query_embedding: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Fallback: Search in local file using cosine similarity
        """
        try:
            # Check if file exists
            if not os.path.exists("bns_vector_data.json"):
                print("📁 No vector data file found. Please run data processing first.")
                return []

            with open("bns_vector_data.json", "r", encoding="utf-8") as f:
                documents = json.load(f)

            if not documents:
                print("📁 Vector data file is empty.")
                return []

            # Calculate cosine similarity
            similarities = []
            query_array = np.array(query_embedding)

            for doc in documents:
                if 'embedding' not in doc:
                    continue
                doc_embedding = np.array(doc['embedding'])
                similarity = np.dot(query_array, doc_embedding) / (
                    np.linalg.norm(query_array) * np.linalg.norm(doc_embedding)
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
            headers = {"api-key": self.api_key}
            
            response = requests.get(
                f"{self.url}/collections/{self.collection_name}/points/{doc_id}",
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                payload = result.get('payload', {})
                return {
                    'id': result.get('id'),
                    'chapter_number': payload.get('chapter_number', ''),
                    'chapter_title': payload.get('chapter_title', ''),
                    'section_number': payload.get('section_number', ''),
                    'section_title': payload.get('section_title', ''),
                    'content': payload.get('content', ''),
                    'full_text': payload.get('full_text', ''),
                    'status': payload.get('status', ''),
                    'jurisdiction': payload.get('jurisdiction', ''),
                    'keywords': payload.get('keywords', []),
                    'cross_references': payload.get('cross_references', []),
                    'penalties': payload.get('penalties', []),
                    'illustrations': payload.get('illustrations', []),
                    'chunk_index': payload.get('chunk_index', 0),
                    'total_chunks': payload.get('total_chunks', 1)
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
        # Qdrant doesn't require explicit connection closing
        pass
