"""
Embeddings + Vector Store (ChromaDB)
Goal: Convert text fragments into numerical vectors
and store them in a database that allows similarity search.
"""
from dotenv import load_dotenv
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from loaders import load_PDF

load_dotenv()
AISTUDIO_APIKEY = os.getenv('AISTUDIO_APIKEY')
PLAYER = "Nikola Jokic"
COLLECTION_NAME = "nikola_jokic_stats"
SQLITE_DISK_DIRECTORY = "./chroma_db"


# Embedding model — (Cast string to vectors).
# Texts with similar meanings generate vectors "close" to each other.
# This is the automatic way of embedding (GoogleGenerativeAIEmbeddings),
# but it can also be done manually.
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001", 
    google_api_key=AISTUDIO_APIKEY
)

# Retrieve the already split PDF from loaders
split_data = load_PDF()

# Create the vector database and store the chunks
vectorstore = Chroma.from_documents(
    documents=split_data,
    embedding=embeddings,
    collection_name=COLLECTION_NAME,
    persist_directory=SQLITE_DISK_DIRECTORY,
)


print("*****************")
print(f"Ingesting PDF data on ChromaDB on collection {COLLECTION_NAME}")
print("*****************")
result = vectorstore._collection.get()

if (result): # Quick simple validation, insufficient to prod env obviosuly
    print("Info indexed on ChromaDB succesfully")

    # Check all documents and last 3 IDS to see behaviour on multiple execs
    print("Checking collection...")
    print(f"Number of splits on collection: {len(result['ids'])}")
    print(f"Last 3 split IDs: {result['ids'][-3:]}")
    print("")