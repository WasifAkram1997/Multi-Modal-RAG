"""
Simple configuration - just load from .env
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Models
LLM_MODEL = "gpt-4o"
EMBEDDING_MODEL = "text-embedding-3-small"

# Paths
CHROMA_DB_PATH = "./chroma_db"
