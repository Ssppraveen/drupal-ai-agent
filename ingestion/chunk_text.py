"""
chunk_text.py

Split cleaned documents into chunks for Azure AI Search.
"""

CHUNK_SIZE = 500


def chunk_documents(documents):
    chunks = []

    for doc in documents:

        text = doc.get("body", "").strip()

        # Skip empty documents
        if not text:
            print(f"⚠️ Skipping '{doc.get('title')}' (empty body)")
            continue

        # Remove extra whitespace
        text = " ".join(text.split())

        # Split into chunks
        for i in range(0, len(text), CHUNK_SIZE):

            chunk = text[i:i + CHUNK_SIZE]

            chunks.append({
                "chunk_id": f"{doc['id']}_{i // CHUNK_SIZE}",
                "document_id": doc["id"],
                "title": doc["title"],
                "content_type": doc["type"],
                "chunk_number": (i // CHUNK_SIZE) + 1,
                "text": chunk,

                # Metadata for Azure AI Search
                "url": doc.get("url", ""),
                "last_modified": doc.get("last_modified", ""),
                "language": "en"
            })

    print(f"\n✅ Created {len(chunks)} chunks")

    return chunks