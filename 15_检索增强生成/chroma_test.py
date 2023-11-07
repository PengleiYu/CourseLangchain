import chromadb
from chromadb.utils import embedding_functions

# default_ef = embedding_functions.DefaultEmbeddingFunction()
# sentence_transformer_embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction()

# client = chromadb.Client()
client = chromadb.PersistentClient()
collection = client.get_or_create_collection(name='my_collection')

# collection.add(documents=["This is a document", "This is another document", ],
#                metadatas=[{'source': 'my_source'}, {'source': 'my_source'}, ],
#                ids=['id1', 'id2', ],
#                )

results = collection.query(query_texts=['This is a query document",'], n_results=2, )
print(results)
