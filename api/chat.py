"""
chat.py

Enterprise AI Chat API
"""

from fastapi import APIRouter
from pydantic import BaseModel

from services.embeddings import generate_query_embedding
from services.vector_search import vector_search
from services.llm import generate_answer

router = APIRouter(tags=["Chat"])


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
def chat(request: ChatRequest):

    # Generate embedding
    embedding = generate_query_embedding(request.question)

    # Retrieve relevant documents
    documents = vector_search(embedding)

    # Generate GPT answer
    answer = generate_answer(request.question, documents)

    # Build citations
    citations = []

    for doc in documents:
        citations.append({
            "title": doc["title"],
            "content_type": doc["content_type"]
        })

    return {
        "question": request.question,
        "answer": answer,
        "citations": citations
    }