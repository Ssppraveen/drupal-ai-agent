"""
services/llm.py

Generate answers using GPT-5 and retrieved Drupal documents.
"""

from openai import OpenAI

from config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_CHAT_DEPLOYMENT,
)

# Initialize Azure OpenAI client
client = OpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    base_url=AZURE_OPENAI_ENDPOINT,
)


def generate_answer(question: str, documents: list):
    """
    Generate an answer using GPT-5 based only on the retrieved documents.
    """

    context = "\n\n".join(
        f"""
Document {i + 1}
Title: {doc.get('title', 'Untitled')}

Content:
{doc.get('text', '')}
"""
        for i, doc in enumerate(documents)
    )

    prompt = f"""
You are an Enterprise AI Assistant.

Your responsibility is to answer employee questions using ONLY the information available in the retrieved Drupal knowledge base.

=========================
INSTRUCTIONS
=========================

1. Carefully read and analyze ALL retrieved documents before answering.
2. Identify the documents that are relevant to the user's question.
3. If multiple documents contain relevant information, combine them into one accurate and complete answer.
4. Ignore unrelated documents.
5. Never use outside knowledge.
6. Never assume or invent information.
7. If the answer is only partially available, answer only with the available information.
8. If the answer cannot be found in the retrieved documents, reply exactly:

"I couldn't find that information in the Drupal knowledge base."

9. Produce only ONE final answer.
10. Do NOT provide summaries, explanations of your reasoning, or multiple answer options.
11. Write naturally and professionally.

=========================
SOURCE CITATION
=========================

After the answer, include only the titles of the documents that you actually used.

Format:

Source:
- Document Title

or

Sources:
- Document Title 1
- Document Title 2

Do not cite documents that were not used.

=========================
KNOWLEDGE BASE
=========================

{context}

=========================
QUESTION
=========================

{question}

=========================
FINAL ANSWER
=========================
"""

    response = client.responses.create(
        model=AZURE_OPENAI_CHAT_DEPLOYMENT,
        input=prompt,
    )

    return response.output_text