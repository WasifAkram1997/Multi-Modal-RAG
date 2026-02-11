"""
Multi-Modal RAG - Simple Version

Usage:
    python main.py ingest <pdf_file>     # Process a PDF
    python main.py query <question>      # Ask a question
"""
import sys
from document_processing import partition_document, chunk_elements
from content_extraction import process_all_chunks
from summarization import create_summary
from vector_store import create_vector_store, load_vector_store
from qa import answer_question


def ingest_document(pdf_path):
    """Process and ingest a PDF document"""
    print("\n" + "="*80)
    print("INGESTING DOCUMENT")
    print("="*80)
    
    # Step 1: Partition PDF
    elements = partition_document(pdf_path)
    
    # Step 2: Chunk elements
    chunks = chunk_elements(elements)
    
    # Step 3: Extract content
    processed_chunks = process_all_chunks(chunks)
    
    # Step 4: Create summaries for hybrid chunks
    print("\nCreating summaries for hybrid chunks...")
    summaries = {}
    for chunk in processed_chunks:
        if chunk["is_hybrid"]:
            summary = create_summary(chunk)
            if summary:
                summaries[chunk["chunk_id"]] = summary
    
    print(f"Created {len(summaries)} summaries")
    
    # Step 5: Create vector store
    db = create_vector_store(processed_chunks, summaries)
    
    print("\n✓ Document ingested successfully!")
    return db


def query_database(question):
    """Query the vector database"""
    print("\n" + "="*80)
    print("QUERYING DATABASE")
    print("="*80)
    
    # Load vector store
    db = load_vector_store()
    
    # Answer question
    answer = answer_question(db, question)
    
    print("\n" + "="*80)
    print("ANSWER:")
    print("="*80)
    print(answer)
    print()


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1]
    
    if command == "ingest":
        if len(sys.argv) < 3:
            print("Usage: python main.py ingest <pdf_file>")
            return
        pdf_path = sys.argv[2]
        ingest_document(pdf_path)
    
    elif command == "query":
        if len(sys.argv) < 3:
            print("Usage: python main.py query <question>")
            return
        question = " ".join(sys.argv[2:])
        query_database(question)
    
    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
