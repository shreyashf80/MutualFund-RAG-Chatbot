"""
Embedding and Indexing module for Mutual Fund FAQ Assistant.
Creates embeddings for text chunks and stores them in ChromaDB.
"""

import os
import shutil
from typing import List, Dict
import logging

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings, HuggingFaceBgeEmbeddings
from langchain.schema import Document
from src.config.settings import (
    EMBEDDING_MODEL,
    CHROMA_PERSIST_DIR,
    CHROMA_COLLECTION_NAME
)

logger = logging.getLogger(__name__)

def get_embeddings_model():
    """Initializes and returns the embedding model."""
    if "bge" in EMBEDDING_MODEL.lower():
        return HuggingFaceBgeEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

_vectorstore_instance = None

def get_vectorstore():
    """Returns the Chroma vector store instance."""
    global _vectorstore_instance
    if _vectorstore_instance is None:
        embeddings = get_embeddings_model()
        _vectorstore_instance = Chroma(
            persist_directory=CHROMA_PERSIST_DIR,
            collection_name=CHROMA_COLLECTION_NAME,
            embedding_function=embeddings
        )
    return _vectorstore_instance

def embed_chunks(chunks: List[Dict]):
    """
    Embeds chunks and stores them in ChromaDB.
    
    Args:
        chunks (List[Dict]): A list of chunk dictionaries containing
                             'page_content' and 'metadata'.
    """
    if not chunks:
        logger.warning("No chunks provided to embed.")
        return
        
    logger.info(f"Embedding {len(chunks)} chunks into ChromaDB...")
    
    vectorstore = get_vectorstore()
    
    documents = [
        Document(page_content=chunk["page_content"], metadata=chunk["metadata"])
        for chunk in chunks
    ]
    
    ids = [chunk["metadata"]["chunk_id"] for chunk in chunks]
    
    vectorstore.add_documents(documents=documents, ids=ids)
    
    logger.info("Successfully embedded chunks and updated vector store.")

def rebuild_index(chunks: List[Dict]):
    """
    Clears the old index completely and builds a new one from scratch.
    
    Args:
        chunks (List[Dict]): Fresh chunks to embed.
    """
    logger.info("Rebuilding index: clearing existing vector store...")
    
    if os.path.exists(CHROMA_PERSIST_DIR):
        try:
            shutil.rmtree(CHROMA_PERSIST_DIR)
            logger.info(f"Deleted existing vector store at {CHROMA_PERSIST_DIR}")
            global _vectorstore_instance
            _vectorstore_instance = None
        except Exception as e:
            logger.error(f"Error deleting vector store: {e}")
            
    # Recreate directory
    os.makedirs(CHROMA_PERSIST_DIR, exist_ok=True)
    
    embed_chunks(chunks)
    logger.info("Index rebuild complete.")
