import os
import json
from typing import List, Dict, Any, Optional
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement
import numpy as np
from dotenv import load_dotenv

load_dotenv()

class DataStaxVectorDB:
    def __init__(self):
        """
        Initialize DataStax Astra DB connection using secure connect bundle
        """
        self.session = None
        self.keyspace = "bns_legal_assistant"
        self.table_name = "bns_sections"
        self.connect()

    def connect(self):
        """
        Connect to DataStax Astra DB using secure connect bundle
        """
        try:
            # Get configuration from environment
            api_token = os.getenv('DATASTAX_API_KEY')
            secure_bundle_path = os.getenv('DATASTAX_SECURE_CONNECT_BUNDLE_PATH')
            
            if not api_token or not secure_bundle_path:
                raise ValueError("DATASTAX_API_KEY and DATASTAX_SECURE_CONNECT_BUNDLE_PATH must be set in environment variables")

            if not os.path.exists(secure_bundle_path):
                raise ValueError(f"Secure connect bundle not found at: {secure_bundle_path}")

            # Configure connection with secure connect bundle
            cloud_config = {
                'secure_connect_bundle': secure_bundle_path
            }

            auth_provider = PlainTextAuthProvider(
                api_token,
                api_token
            )

            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            self.session = cluster.connect()

            # Create keyspace if it doesn't exist
            self.create_keyspace()
            self.session.set_keyspace(self.keyspace)

            # Create table if it doesn't exist
            self.create_table()

            print("✅ Connected to DataStax Astra DB using secure connect bundle")

        except Exception as e:
            print(f"❌ Error connecting to DataStax: {e}")
            # Fallback to local file storage for development
            self.use_file_storage = True
            print("📁 Using local file storage as fallback")

    def create_keyspace(self):
        """
        Create keyspace for BNS data
        """
        try:
            self.session.execute(f"""
                CREATE KEYSPACE IF NOT EXISTS {self.keyspace}
                WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': 1}}
            """)
        except Exception as e:
            print(f"Warning: Could not create keyspace: {e}")

    def create_table(self):
        """
        Create table for storing BNS sections with vector support
        """
        try:
            self.session.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id text PRIMARY KEY,
                    chapter_number text,
                    chapter_title text,
                    section_number text,
                    section_title text,
                    content text,
                    full_text text,
                    status text,
                    jurisdiction text,
                    keywords list<text>,
                    cross_references list<text>,
                    penalties list<text>,
                    illustrations list<text>,
                    chunk_index int,
                    total_chunks int,
                    embedding list<float>,
                    created_at timestamp
                )
            """)
        except Exception as e:
            print(f"Warning: Could not create table: {e}")

    def insert_documents(self, documents: List[Dict[str, Any]]):
        """
        Insert documents into the vector database
        """
        if hasattr(self, 'use_file_storage') and self.use_file_storage:
            return self.insert_to_file(documents)

        try:
            insert_query = f"""
                INSERT INTO {self.table_name} (
                    id, chapter_number, chapter_title, section_number, section_title,
                    content, full_text, status, jurisdiction, keywords, cross_references,
                    penalties, illustrations, chunk_index, total_chunks, embedding, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, toTimestamp(now()))
            """

            prepared = self.session.prepare(insert_query)

            for doc in documents:
                self.session.execute(prepared, (
                    doc['id'],
                    doc['chapter_number'],
                    doc['chapter_title'],
                    doc['section_number'],
                    doc['section_title'],
                    doc['content'],
                    doc['full_text'],
                    doc['status'],
                    doc['jurisdiction'],
                    doc['keywords'],
                    doc['cross_references'],
                    doc['penalties'],
                    doc['illustrations'],
                    doc['chunk_index'],
                    doc['total_chunks'],
                    doc['embedding']
                ))

            print(f"✅ Inserted {len(documents)} documents into DataStax")

        except Exception as e:
            print(f"❌ Error inserting into DataStax: {e}")
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
        Search for similar documents using vector similarity
        """
        if hasattr(self, 'use_file_storage') and self.use_file_storage:
            return self.search_in_file(query_embedding, limit)

        try:
            # For DataStax with vector search, you would use vector similarity
            # This is a simplified version - you'll need to implement proper vector search
            query = f"""
                SELECT * FROM {self.table_name}
                ORDER BY embedding <-> ?
                LIMIT {limit}
            """

            # Note: This is a placeholder. Actual vector search implementation
            # depends on your DataStax setup and vector search capabilities

            results = []
            # Implementation would go here
            return results

        except Exception as e:
            print(f"❌ Error searching in DataStax: {e}")
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
            query = f"SELECT * FROM {self.table_name} WHERE id = ?"
            result = self.session.execute(query, [doc_id])
            row = result.one()

            if row:
                return dict(row._asdict())
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
        if self.session:
            self.session.shutdown() 