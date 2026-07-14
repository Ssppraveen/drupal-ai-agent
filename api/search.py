"""
search.py

Simple Azure AI Search API
"""

from fastapi import APIRouter
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

from config import (
    AZURE_SEARCH_ENDPOINT,
    AZURE_SEARCH_API_KEY,
    AZURE_SEARCH_INDEX,
)

router = APIRouter(tags=["Search"])

# Azure AI Search Client
client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(AZURE_SEARCH_API_KEY),
)


@router.get("/search-test")
def search_test():

    results = client.search(
        search_text="*",
        top=5,
    )

    documents = []

    for doc in results:

        documents.append({
            "title": doc.get("title"),
            "content_type": doc.get("content_type"),
            "chunk_number": doc.get("chunk_number"),
            "text": doc.get("text"),
        })

    return {
        "count": len(documents),
        "documents": documents,
    }