"""
search_index.py

Create Azure AI Search Vector Index
"""

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    AzureOpenAIVectorizer,
    AzureOpenAIVectorizerParameters,
)

from config import (
    AZURE_SEARCH_ENDPOINT,
    AZURE_SEARCH_API_KEY,
    AZURE_SEARCH_INDEX,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
)

# ---------------------------------------------
# Search Client
# ---------------------------------------------

client = SearchIndexClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    credential=AzureKeyCredential(AZURE_SEARCH_API_KEY),
)

# ---------------------------------------------
# Vector Search
# ---------------------------------------------

vector_search = VectorSearch(
    algorithms=[
        HnswAlgorithmConfiguration(
            name="hnsw-config"
        )
    ],
    profiles=[
        VectorSearchProfile(
            name="vector-profile",
            algorithm_configuration_name="hnsw-config",
        )
    ]
)

# ---------------------------------------------
# Index Fields
# ---------------------------------------------

fields = [

    SimpleField(
        name="chunk_id",
        type=SearchFieldDataType.String,
        key=True,
    ),

    SimpleField(
        name="document_id",
        type=SearchFieldDataType.String,
        filterable=True,
    ),

    SearchableField(
        name="title",
        type=SearchFieldDataType.String,
    ),

    SearchableField(
        name="content_type",
        type=SearchFieldDataType.String,
    ),

    SearchableField(
        name="text",
        type=SearchFieldDataType.String,
    ),

    SearchField(
        name="embedding",
        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        searchable=True,
        vector_search_dimensions=1536,
        vector_search_profile_name="vector-profile",
    ),

    SimpleField(
        name="chunk_number",
        type=SearchFieldDataType.Int32,
    ),
]

index = SearchIndex(
    name=AZURE_SEARCH_INDEX,
    fields=fields,
    vector_search=vector_search,
)

print("=" * 60)
print("Creating Azure AI Search Index")
print("=" * 60)

try:

    client.create_or_update_index(index)

    print("\n✅ Index created successfully")
    print(f"Index Name : {AZURE_SEARCH_INDEX}")

except Exception as e:

    print("\n❌ Failed")
    print(e)