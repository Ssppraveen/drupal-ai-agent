"""
services/vector_search.py

Perform vector search in Azure AI Search.
"""

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

from config import (
    AZURE_SEARCH_ENDPOINT,
    AZURE_SEARCH_API_KEY,
    AZURE_SEARCH_INDEX,
)

client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(AZURE_SEARCH_API_KEY),
)


def vector_search(embedding, top=5):
    """
    Search Azure AI Search using a vector embedding.
    """

    vector_query = VectorizedQuery(
        vector=embedding,
        k_nearest_neighbors=top,
        fields="embedding",
    )

    results = client.search(
        search_text=None,
        vector_queries=[vector_query],
        top=top,
    )

    documents = []

    for doc in results:
        documents.append({
            "title": doc["title"],
            "content_type": doc["content_type"],
            "text": doc["text"],
            "chunk_number": doc["chunk_number"],
        })

    return documents