import boto3
import json
from rag_utils import load_documents_from_folder, load_faiss_index, query_faiss

# Claude 3 Haiku model ID
MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"

# Connect to Bedrock
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

def generate_dispute_reply(invoice_text, query_text=None):
    # Load FAISS index + documents
    all_docs, _ = load_documents_from_folder("data")
    index, _ = load_faiss_index()

    # Use the invoice content as the search query if no specific query
    query = query_text or invoice_text

    # Get top 2 relevant past documents
    relevant_chunks = query_faiss(query, index, all_docs, k=2)

    user_prompt = f"""
Disputed Invoice:
{invoice_text}

Relevant Past Documents (POs/SOs):
1. {relevant_chunks[0][:1000]}
2. {relevant_chunks[1][:1000]}

Please draft a helpful email reply that addresses the issue clearly.
"""

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "messages": [
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.3
    }

    # Invoke Claude
    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())
    return result["content"][0]["text"]
