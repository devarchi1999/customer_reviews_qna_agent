# import chromadb
import pandas as pd
import numpy as np
from uuid import uuid4
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
from db_utils import batch_iterator
from tqdm import tqdm

load_dotenv(".env")

# create embeddings
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

#reading api key from environment variable
pinecone_api_key = os.environ.get("PINECONE_API_KEY")
pinecone_namespace = os.environ.get("PINECONE_NAMESPACE")
pinecone_index_name = os.environ.get("PINECONE_INDEX_NAME")

# initializing pinecone client
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(pinecone_index_name)
# vector_store = PineconeVectorStore(index=index, embedding=embeddings)

#getting the reviews dataset
reviews = pd.read_csv('data/processed_reviews.csv')
reviews['review_text'] = reviews['review_text'].astype(str)

#embedding creation
try:
    print('embedding creation started')
    embeddings = embedding_model.encode(reviews['review_text'].tolist(), show_progress_bar=True)
    print('embeddings created successfully')
except Exception as e:
    print(f"An error occurred during embedding creation: {e}")
 
#metadata creation    
try:
    print('metadata creation started')
    metadata = [{'sentiment': row['sentiment'],
                 'region': row['region'],
                 'store': row['store'],
                 'review_text': row['review_text']} for _, row in reviews.iterrows()]
    ids = [str(uuid4()) for _ in range(reviews.shape[0])]
    print('metadata created successfully')
except Exception as e:
    print(f"An error occurred during metadata creation: {e}")

# preparing data for upsert
try:
    print('preparing data for upsert started')
    pinecone_documents = [{'id': ids[i],
                      'values': embeddings[i],
                        'metadata': metadata[i]} for i in range(reviews.shape[0])]
    print('data prepared successfully')
except Exception as e:
    print(f"An error occurred during data preparation: {e}")
    
# batch upsert to pinecone
try:
    print(f"Total documents to upsert: {len(pinecone_documents)}")
    for batch in tqdm(batch_iterator(pinecone_documents, batch_size=200)):
        print(f"Upserting batch of size: {len(batch)}")
        index.upsert(vectors=batch, namespace=pinecone_namespace)
        print("Batch upserted successfully.")
except Exception as e:
    print(f"An error occurred while upserting batch: {e}")


