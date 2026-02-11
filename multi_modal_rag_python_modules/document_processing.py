"""
Document processing functions
"""
from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title


def partition_document(file_path: str):
    """Extract elements from PDF"""
    print(f"Partitioning document: {file_path}")
    
    elements = partition_pdf(
        filename=file_path,
        strategy="hi_res",
        infer_table_structure=True,
        extract_image_block_types=["Image"],
        extract_image_block_to_payload=True
    )
    
    print(f"Extracted {len(elements)} elements")
    return elements


def chunk_elements(elements):
    """Chunk elements by title"""
    print(f"Chunking {len(elements)} elements")
    
    chunks = chunk_by_title(
        elements,
        max_characters=4000,
        new_after_n_chars=3800,
        combine_text_under_n_chars=2000
    )
    
    print(f"Created {len(chunks)} chunks")
    return chunks
