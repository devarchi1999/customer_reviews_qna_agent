#vector db retrieval
from sentence_transformers import SentenceTransformer
from pinecone.grpc import PineconeGRPC as Pinecone
import os
from dotenv import load_dotenv

load_dotenv(".env")

#reading api key from environment variable
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
pinecone_namespace = os.environ.get("PINECONE_NAMESPACE")
pinecone_index_name = os.environ.get("PINECONE_INDEX_NAME")
embedding_model_name = os.environ.get("EMBEDDING_MODEL_NAME")

# initializing pinecone client
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(pinecone_index_name)

# Retrieval class with filtering capability
class RetrievalWithFilter:
    def __init__(self):
        self.embedding_model = SentenceTransformer(embedding_model_name)


    def retrieve(self, query, top_k=10, filter=None) -> dict:
        self.query = query
        self.query_embedding = self.embedding_model.encode([query])[0]
        response = index.query(namespace=pinecone_namespace,
                                vector=self.query_embedding, 
                                top_k=top_k,
                                filter=filter,
                                include_metadata=True,
                                include_values=False
                                )
        return response
 
# Embedding generator class    
class EmbeddingGenerator:
    def __init__(self):
        self.embedding_model = SentenceTransformer(embedding_model_name)

    def generate_embedding(self, text:str) -> list[float]:
        embedding = self.embedding_model.encode([text])[0]
        return embedding
    
    
# if __name__ == "__main__":
#     retriever = RetrievalWithFilter()
#     response = retriever.retrieve(query="Great customer service in region1 store2", top_k=5,
#                                  filter={"region":{"$in":["region1"]},"store":{"$in":["store2"]}})
#     for match in response['matches']:
#         print(match['metadata']['review_text'])
        
        



