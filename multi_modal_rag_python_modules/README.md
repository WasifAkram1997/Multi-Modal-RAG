# Multi-Modal RAG - Simple Version

A straightforward implementation of multi-modal RAG that processes PDFs with text, tables, and images.

## Project Structure

```
multi_modal_rag_simple/
├── config.py                    # Configuration
├── document_processing.py       # PDF partitioning & chunking
├── content_extraction.py        # Extract text, tables, images
├── summarization.py             # AI summaries for hybrid chunks
├── vector_store.py              # ChromaDB operations
├── qa.py                        # Question answering
├── main.py                      # Main script
├── requirements.txt             # Dependencies
└── .env.example                 # Environment template
```

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Add your OpenAI API key to .env
```

## Usage

### 1. Ingest a PDF

```bash
python main.py ingest your_document.pdf
```

This will:
- Extract text, tables, and images
- Create chunks
- Generate summaries for hybrid content
- Store in ChromaDB

### 2. Ask Questions

```bash
python main.py query "What is the main topic?"
```

## Use in Your Code

```python
from document_processing import partition_document, chunk_elements
from content_extraction import process_all_chunks
from summarization import create_summary
from vector_store import create_vector_store
from qa import answer_question

# Ingest
elements = partition_document("document.pdf")
chunks = chunk_elements(elements)
processed = process_all_chunks(chunks)

summaries = {}
for chunk in processed:
    if chunk["is_hybrid"]:
        summary = create_summary(chunk)
        if summary:
            summaries[chunk["chunk_id"]] = summary

db = create_vector_store(processed, summaries)

# Query
answer = answer_question(db, "Your question?")
print(answer)
```

## What Each File Does

- **config.py** - Just loads environment variables
- **document_processing.py** - Partitions PDF and chunks it
- **content_extraction.py** - Gets text, tables, images from chunks
- **summarization.py** - Creates AI summaries for hybrid chunks
- **vector_store.py** - Saves to and loads from ChromaDB
- **qa.py** - Answers questions using retrieved content
- **main.py** - Command-line interface

Simple and straightforward! 🚀
