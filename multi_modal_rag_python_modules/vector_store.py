"""
Vector database operations
"""
import json
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
import config


def create_vector_store(processed_chunks, summaries=None):
    """Create vector store from processed chunks"""
    print("Creating vector store")
    
    summaries = summaries or {}
    documents = []
    
    for chunk in processed_chunks:
        chunk_id = chunk["chunk_id"]
        content = chunk["content"]
        
        # Use summary if available, otherwise use raw text
        if chunk_id in summaries:
            embedding_text = summaries[chunk_id]
        else:
            embedding_text = content["raw_text"]
        
        # Store original content in metadata
        metadata = {
            "chunk_id": chunk_id,
            "original_content": json.dumps(content),
            "has_tables": chunk["has_tables"],
            "has_images": chunk["has_images"]
        }
        
        doc = Document(page_content=embedding_text, metadata=metadata)
        documents.append(doc)
    
    # Create ChromaDB
    embeddings = OpenAIEmbeddings(model=config.EMBEDDING_MODEL)
    
    db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=config.CHROMA_DB_PATH
    )
    
    print(f"Vector store created with {len(documents)} documents")
    return db


def load_vector_store():
    """Load existing vector store"""
    print("Loading vector store")
    
    embeddings = OpenAIEmbeddings(model=config.EMBEDDING_MODEL)
    
    db = Chroma(
        embedding_function=embeddings,
        persist_directory=config.CHROMA_DB_PATH
    )
    
    return db
