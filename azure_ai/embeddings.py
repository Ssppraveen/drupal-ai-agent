"""
embeddings.py

Generate embeddings using Azure AI Foundry (OpenAI v1 API)
"""

import json
import time
from pathlib import Path

from openai import OpenAI

from config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
)

client = OpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    base_url=AZURE_OPENAI_ENDPOINT,
)


def generate_embedding(text: str):
    response = client.embeddings.create(
        model=AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
        input=text,
    )
    return response.data[0].embedding


def generate_embeddings():

    input_file = Path("output/chunks.json")
    output_file = Path("output/chunks_with_embeddings.json")

    with open(input_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print("=" * 60)
    print("Generating Azure AI Foundry Embeddings")
    print("=" * 60)

    success = 0

    for i, chunk in enumerate(chunks, start=1):

        print(f"[{i}/{len(chunks)}] {chunk['title']}")

        try:
            embedding = generate_embedding(chunk["text"])
            chunk["embedding"] = embedding
            success += 1

        except Exception as e:
            print(e)
            chunk["embedding"] = None

        time.sleep(0.2)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    print("\n" + "=" * 60)
    print(f"Success : {success}/{len(chunks)}")
    print(f"Saved to: {output_file}")
    print("=" * 60)


if __name__ == "__main__":
    generate_embeddings()