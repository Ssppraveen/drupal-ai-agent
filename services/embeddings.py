"""
services/embeddings.py

Generate embeddings for user questions using Azure AI Foundry.
"""

from openai import OpenAI

from config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
)

# Azure AI Foundry Client
client = OpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    base_url=AZURE_OPENAI_ENDPOINT,
)


def generate_query_embedding(question: str):
    """
    Generate an embedding vector for a user question.
    """

    response = client.embeddings.create(
        model=AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
        input=question,
    )

    return response.data[0].embedding