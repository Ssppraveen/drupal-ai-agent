"""
clean_html.py

Convert Drupal HTML into clean plain text.
"""

from bs4 import BeautifulSoup


def clean_documents(documents):
    """
    Clean HTML from all documents.
    """

    cleaned_documents = []

    for doc in documents:

        html = doc.get("body", "")

        soup = BeautifulSoup(html, "html.parser")

        clean_text = soup.get_text(separator="\n", strip=True)

        cleaned_doc = doc.copy()
        cleaned_doc["body"] = clean_text

        cleaned_documents.append(cleaned_doc)

    return cleaned_documents