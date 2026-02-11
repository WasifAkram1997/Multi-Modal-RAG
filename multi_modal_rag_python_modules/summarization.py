"""
Create AI summaries for hybrid chunks
"""
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import config


def create_summary(processed_chunk):
    """Create AI summary for hybrid chunks"""
    if not processed_chunk["is_hybrid"]:
        return None
    
    content = processed_chunk["content"]
    chunk_id = processed_chunk["chunk_id"]
    
    print(f"Creating summary for chunk {chunk_id}")
    
    try:
        llm = ChatOpenAI(model=config.LLM_MODEL, temperature=0)
        
        # Build prompt
        prompt_text = f"""Summarize the following content:

TEXT:
{content['raw_text']}

"""
        if content["tables_html"]:
            prompt_text += f"TABLES: {len(content['tables_html'])} table(s)\n"
            for i, table in enumerate(content["tables_html"], 1):
                prompt_text += f"\nTable {i}:\n{table}\n"
        
        if content["images_base64"]:
            prompt_text += f"\nIMAGES: {len(content['images_base64'])} image(s) attached\n"
        
        prompt_text += "\nCreate a comprehensive summary that captures all content."
        
        # Build message with images
        message_content = [{"type": "text", "text": prompt_text}]
        
        for image_base64 in content["images_base64"]:
            message_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
            })
        
        # Generate summary
        message = HumanMessage(content=message_content)
        response = llm.invoke([message])
        
        return response.content.strip()
        
    except Exception as e:
        print(f"  Failed: {e}")
        return None
