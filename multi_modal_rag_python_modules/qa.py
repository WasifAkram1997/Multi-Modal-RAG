"""
Question answering
"""
import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import config


def answer_question(db, question, k=3):
    """Answer a question using the vector database"""
    print(f"\nQuestion: {question}")
    
    # Retrieve relevant chunks
    retriever = db.as_retriever(search_kwargs={"k": k})
    chunks = retriever.invoke(question)
    
    print(f"Retrieved {len(chunks)} relevant chunks")
    
    # Generate answer
    llm = ChatOpenAI(model=config.LLM_MODEL, temperature=0)
    
    # Build prompt
    prompt_text = f"""Based on the following documents, answer this question: {question}

DOCUMENTS:
"""
    
    for i, chunk in enumerate(chunks, 1):
        prompt_text += f"\n--- Document {i} ---\n"
        prompt_text += f"{chunk.page_content}\n"
        
        # Add original content if available
        if "original_content" in chunk.metadata:
            original = json.loads(chunk.metadata["original_content"])
            
            # Add tables
            if original.get("tables_html"):
                prompt_text += "\nTABLES:\n"
                for j, table in enumerate(original["tables_html"], 1):
                    prompt_text += f"Table {j}:\n{table}\n\n"
            
            # Note images
            if original.get("images_base64"):
                prompt_text += f"[Contains {len(original['images_base64'])} image(s)]\n"
    
    prompt_text += "\nProvide a clear answer. Cite document numbers if relevant.\n\nANSWER:"
    
    # Build message with images
    message_content = [{"type": "text", "text": prompt_text}]
    
    # Add all images
    for chunk in chunks:
        if "original_content" in chunk.metadata:
            original = json.loads(chunk.metadata["original_content"])
            for image_base64 in original.get("images_base64", []):
                message_content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                })
    
    # Generate answer
    message = HumanMessage(content=message_content)
    response = llm.invoke([message])
    
    return response.content
