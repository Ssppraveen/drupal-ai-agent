"""
run_pipeline.py

Complete Drupal ingestion pipeline.
"""

from ingestion.fetch_content import fetch_content
from ingestion.clean_html import clean_documents
from ingestion.chunk_text import chunk_documents
from ingestion.save_json import save_json

# Import embedding generation
from azure_ai.embeddings import generate_embeddings


def run_pipeline():

    print("=" * 60)
    print("Drupal AI Agent - Ingestion Pipeline")
    print("=" * 60)

    # --------------------------------------------------
    # Step 1: Fetch content from Drupal
    # --------------------------------------------------
    documents = fetch_content()

    # --------------------------------------------------
    # Step 2: Clean HTML
    # --------------------------------------------------
    cleaned_documents = clean_documents(documents)

    # --------------------------------------------------
    # Step 3: Chunk documents
    # --------------------------------------------------
    chunks = chunk_documents(cleaned_documents)

    # --------------------------------------------------
    # Step 4: Save JSON files
    # --------------------------------------------------
    save_json(cleaned_documents, "documents.json")
    save_json(chunks, "chunks.json")

    # --------------------------------------------------
    # Step 5: Generate embeddings
    # --------------------------------------------------
    print("\nGenerating embeddings...")
    generate_embeddings()

    print("\n" + "=" * 60)
    print("Pipeline completed successfully!")
    print("=" * 60)

    print(f"Documents : {len(cleaned_documents)}")
    print(f"Chunks    : {len(chunks)}")


if __name__ == "__main__":
    run_pipeline()