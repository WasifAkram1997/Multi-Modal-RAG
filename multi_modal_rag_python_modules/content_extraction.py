"""
Extract text, tables, and images from chunks
"""
import json


def extract_content(chunk):
    """Extract all content types from a chunk"""
    content = {
        "raw_text": str(chunk),
        "tables_html": [],
        "images_base64": []
    }
    
    # Get metadata if available
    if hasattr(chunk, "metadata"):
        metadata = chunk.metadata.to_dict()
        
        # Extract table HTML
        if "text_as_html" in metadata and metadata.get("text_as_html"):
            content["tables_html"].append(metadata["text_as_html"])
        
        # Extract image base64
        if "image_base64" in metadata and metadata.get("image_base64"):
            content["images_base64"].append(metadata["image_base64"])
    
    return content


def process_all_chunks(chunks):
    """Process all chunks and extract content"""
    print(f"Processing {len(chunks)} chunks")
    
    processed = []
    for i, chunk in enumerate(chunks, 1):
        content = extract_content(chunk)
        
        # Determine content type
        has_tables = len(content["tables_html"]) > 0
        has_images = len(content["images_base64"]) > 0
        is_hybrid = has_tables or has_images
        
        processed.append({
            "chunk_id": i,
            "content": content,
            "has_tables": has_tables,
            "has_images": has_images,
            "is_hybrid": is_hybrid
        })
        
        if is_hybrid:
            print(f"  Chunk {i}: Hybrid (Tables: {len(content['tables_html'])}, Images: {len(content['images_base64'])})")
    
    return processed
