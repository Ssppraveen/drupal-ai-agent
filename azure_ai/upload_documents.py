"""
upload_documents.py

Upload documents with embeddings to Azure AI Search.
"""

import json
from pathlib import Path

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from config import (
    AZURE_SEARCH_ENDPOINT,
    AZURE_SEARCH_API_KEY,
    AZURE_SEARCH_INDEX,
)

# =====================================================
# Azure AI Search Client
# =====================================================

client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(AZURE_SEARCH_API_KEY),
)

# =====================================================
# Load chunks
# =====================================================

input_file = Path("output/chunks_with_embeddings.json")

if not input_file.exists():
    raise FileNotFoundError(
        "chunks_with_embeddings.json not found. Run embeddings.py first."
    )

with open(input_file, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print("=" * 60)
print("Uploading Documents to Azure AI Search")
print("=" * 60)

documents = []

for chunk in chunks:

    embedding = chunk.get("embedding")

    # Skip documents without embeddings
    if not embedding:
        continue

    documents.append({
        "chunk_id": chunk["chunk_id"],
        "document_id": chunk["document_id"],
        "title": chunk["title"],
        "content_type": chunk["content_type"],
        "text": chunk["text"],
        "embedding": embedding,
        "chunk_number": chunk["chunk_number"],
    })

print(f"\nDocuments ready for upload : {len(documents)}")

if len(documents) == 0:
    raise Exception("No documents available for upload.")

# =====================================================
# Upload
# =====================================================

results = client.upload_documents(documents)

success = 0
failed = 0

for result in results:
    if result.succeeded:
        success += 1
    else:
        failed += 1
        print(f"❌ Failed document: {result.key}")

print("\n" + "=" * 60)
print(f"Uploaded Successfully : {success}")
print(f"Failed                : {failed}")
print("=" * 60)

if failed == 0:
    print("\n🎉 All documents uploaded successfully!")
else:
    print("\n⚠️ Some documents failed to upload.")