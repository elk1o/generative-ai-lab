"""
Embeddings + Vector Store (ChromaDB)
Goal: Convert text fragments into numerical vectors
and store them in a database that allows similarity search.
"""
from dotenv import load_dotenv
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from multiple_sources_loaders import load_multiple_PDFs

load_dotenv()
AISTUDIO_APIKEY = os.getenv('AISTUDIO_APIKEY')
MULTIPLE_SOURCES_COLLECTION_NAME = os.getenv('MULTIPLE_SOURCES_COLLECTION_NAME')
SQLITE_DISK_DIRECTORY = os.getenv('SQLITE_DISK_DIRECTORY')
CHROMADB_EMBEDDINGS_MODEL = os.getenv('CHROMADB_EMBEDDINGS_MODEL')

# Embedding model — (Cast string to vectors).
# Texts with similar meanings generate vectors "close" to each other.
# This is the automatic way of embedding (GoogleGenerativeAIEmbeddings),
# but it can also be done manually.
embeddings = GoogleGenerativeAIEmbeddings(
    model=CHROMADB_EMBEDDINGS_MODEL, 
    google_api_key=AISTUDIO_APIKEY
)

# Retrieve the already split PDF from loaders
split_data = load_multiple_PDFs()

# Create the vector database and store the chunks
vectorstore = Chroma.from_documents(
    documents=split_data,
    embedding=embeddings,
    collection_name=MULTIPLE_SOURCES_COLLECTION_NAME,
    persist_directory=SQLITE_DISK_DIRECTORY,
)


print("*****************")
print(f"Ingesting PDF data on ChromaDB on collection {MULTIPLE_SOURCES_COLLECTION_NAME}")
print("*****************")
result = vectorstore._collection.get()
collection_name = vectorstore._collection.name

if (result): # Quick simple validation, insufficient to prod env obviosuly
    print(f"Info indexed on ChromaDB on collection {collection_name} succesfully")

    # Check all documents and last 3 IDS to see behaviour on multiple execs
    print(f"Checking collection {collection_name} ...")
    print(f"Number of splits on collection: {len(result['ids'])}")
    print(f"Last 3 split IDs: {result['ids'][-3:]}")
    print("")