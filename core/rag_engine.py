"""
RAG (Retrieval-Augmented Generation) Engine for context-aware agent responses.
"""

import os
from typing import List, Dict, Optional
from pathlib import Path
import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.docstore.document import Document as LangchainDocument
from loguru import logger


class RAGEngine:
    """Manages document indexing and retrieval for RAG."""
    
    def __init__(self, 
                 vector_db_path: str = "./vector_db",
                 collection_name: str = "test_automation_docs",
                 chunk_size: int = 1000,
                 chunk_overlap: int = 200):
        """
        Initialize RAG engine.
        
        Args:
            vector_db_path: Path to store vector database
            collection_name: Name of the collection
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.vector_db_path = Path(vector_db_path)
        self.vector_db_path.mkdir(parents=True, exist_ok=True)
        
        self.collection_name = collection_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Initialize embeddings
        try:
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001"
            )
            logger.info("Google embeddings initialized")
        except Exception as e:
            logger.error(f"Failed to initialize embeddings: {str(e)}")
            raise
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(self.vector_db_path),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
            logger.info(f"Loaded existing collection: {collection_name}")
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"description": "Test automation documentation"}
            )
            logger.info(f"Created new collection: {collection_name}")
        
        # Text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
    
    def add_documents(self, documents: List[Dict]) -> int:
        """
        Add documents to the vector database.
        
        Args:
            documents: List of document dictionaries with 'text' and 'metadata'
            
        Returns:
            Number of chunks added
        """
        all_chunks = []
        chunk_count = 0
        
        for doc in documents:
            if not doc or 'text' not in doc:
                continue
            
            text = doc['text']
            metadata = doc.get('metadata', {})
            source = doc.get('source', 'unknown')
            doc_type = doc.get('type', 'unknown')
            
            # Split text into chunks
            chunks = self.text_splitter.split_text(text)
            
            for i, chunk in enumerate(chunks):
                chunk_metadata = {
                    'source': source,
                    'type': doc_type,
                    'chunk_index': i,
                    'total_chunks': len(chunks),
                    **metadata
                }
                
                all_chunks.append({
                    'text': chunk,
                    'metadata': chunk_metadata,
                    'id': f"{source}_{i}"
                })
                chunk_count += 1
        
        if not all_chunks:
            logger.warning("No chunks to add")
            return 0
        
        # Generate embeddings
        try:
            texts = [chunk['text'] for chunk in all_chunks]
            metadatas = [chunk['metadata'] for chunk in all_chunks]
            ids = [chunk['id'] for chunk in all_chunks]
            
            # Generate embeddings using Google
            embeddings_list = []
            batch_size = 100
            
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                batch_embeddings = self.embeddings.embed_documents(batch)
                embeddings_list.extend(batch_embeddings)
            
            # Add to ChromaDB
            self.collection.add(
                embeddings=embeddings_list,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added {chunk_count} chunks to vector database")
            return chunk_count
            
        except Exception as e:
            logger.error(f"Error adding documents to vector database: {str(e)}")
            return 0
    
    def query(self, 
              query_text: str, 
              n_results: int = 5,
              filter_dict: Optional[Dict] = None) -> List[Dict]:
        """
        Query the vector database.
        
        Args:
            query_text: Query text
            n_results: Number of results to return
            filter_dict: Optional metadata filters
            
        Returns:
            List of relevant documents
        """
        try:
            # Generate query embedding
            query_embedding = self.embeddings.embed_query(query_text)
            
            # Query ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=filter_dict
            )
            
            # Format results
            formatted_results = []
            
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    formatted_results.append({
                        'text': doc,
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results['distances'] else None
                    })
            
            logger.info(f"Retrieved {len(formatted_results)} results for query")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error querying vector database: {str(e)}")
            return []
    
    def get_context_for_agent(self, 
                               query: str, 
                               agent_type: str = None,
                               max_tokens: int = 4000) -> str:
        """
        Get relevant context for an agent query.
        
        Args:
            query: Agent's query
            agent_type: Type of agent (for filtering)
            max_tokens: Maximum tokens in context
            
        Returns:
            Formatted context string
        """
        # Build filter if agent type specified
        filter_dict = None
        if agent_type:
            filter_dict = {"type": agent_type}
        
        # Query vector database
        results = self.query(query, n_results=10, filter_dict=filter_dict)
        
        # Build context string
        context_parts = []
        total_length = 0
        
        for result in results:
            text = result['text']
            source = result['metadata'].get('source', 'unknown')
            
            # Estimate tokens (rough: 1 token ≈ 4 chars)
            text_tokens = len(text) // 4
            
            if total_length + text_tokens > max_tokens:
                break
            
            context_parts.append(f"[Source: {source}]\n{text}\n")
            total_length += text_tokens
        
        context = "\n---\n".join(context_parts)
        
        if context:
            logger.info(f"Generated context of ~{total_length} tokens")
        else:
            logger.warning("No relevant context found")
        
        return context
    
    def delete_collection(self):
        """Delete the current collection."""
        try:
            self.client.delete_collection(name=self.collection_name)
            logger.info(f"Deleted collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error deleting collection: {str(e)}")
    
    def get_stats(self) -> Dict:
        """Get statistics about the vector database."""
        try:
            count = self.collection.count()
            
            return {
                'collection_name': self.collection_name,
                'total_documents': count,
                'vector_db_path': str(self.vector_db_path)
            }
        except Exception as e:
            logger.error(f"Error getting stats: {str(e)}")
            return {}
    
    def search_by_metadata(self, metadata_filter: Dict, limit: int = 10) -> List[Dict]:
        """
        Search documents by metadata.
        
        Args:
            metadata_filter: Metadata filter dictionary
            limit: Maximum results
            
        Returns:
            List of matching documents
        """
        try:
            results = self.collection.get(
                where=metadata_filter,
                limit=limit
            )
            
            formatted_results = []
            if results['documents']:
                for i, doc in enumerate(results['documents']):
                    formatted_results.append({
                        'text': doc,
                        'metadata': results['metadatas'][i] if results['metadatas'] else {}
                    })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching by metadata: {str(e)}")
            return []
