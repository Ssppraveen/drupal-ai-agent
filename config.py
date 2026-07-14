import os
from dotenv import load_dotenv

load_dotenv("docker/.env")

# ==========================
# Drupal
# ==========================

DRUPAL_URL = os.getenv("DRUPAL_URL")
JSON_API_URL = os.getenv("JSON_API_URL")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "output")

# ==========================
# Azure OpenAI
# ==========================

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_CHAT_DEPLOYMENT = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

# ==========================
# Azure AI Search
# ==========================

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX")