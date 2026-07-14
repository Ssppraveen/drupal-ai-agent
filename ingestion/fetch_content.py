"""
fetch_content.py

Fetch all Pages and Articles from Drupal JSON:API
"""

import requests
from config import DRUPAL_URL

# Content types to fetch
CONTENT_TYPES = [
    "page",
    "article"
]


def extract_body(attributes):
    """
    Safely extract body HTML from a Drupal node.
    Returns an empty string if body doesn't exist.
    """
    body = attributes.get("body")

    if isinstance(body, dict):
        return body.get("processed", "")

    return ""


def fetch_content():

    all_content = []

    for content_type in CONTENT_TYPES:

        url = f"{DRUPAL_URL}/jsonapi/node/{content_type}"

        print(f"\nFetching {content_type}...")
        print(f"URL: {url}")

        try:

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()

            items = data.get("data", [])

            print(f"Found {len(items)} {content_type}(s)")

            for item in items:

                attributes = item.get("attributes", {})
                links = item.get("links", {})

                document = {

                    # Unique ID
                    "id": item.get("id"),

                    # Content Type
                    "type": content_type,

                    # Title
                    "title": attributes.get("title", "Untitled"),

                    # HTML Body
                    "body": extract_body(attributes),

                    # Metadata
                    "status": attributes.get("status", True),
                    "created": attributes.get("created"),
                    "changed": attributes.get("changed"),
                    "langcode": attributes.get("langcode", "en"),

                    # Drupal API URL
                    "self_url": links.get("self", {}).get("href", "")
                }

                all_content.append(document)

            print(f"✅ Successfully fetched {len(items)} {content_type}(s)")

        except Exception as e:

            print(f"❌ Error fetching {content_type}")
            print(e)

    return all_content


if __name__ == "__main__":

    documents = fetch_content()

    print("\n" + "=" * 60)
    print(f"Total Documents: {len(documents)}")
    print("=" * 60)

    for doc in documents:

        print(f"[{doc['type']}] {doc['title']}")