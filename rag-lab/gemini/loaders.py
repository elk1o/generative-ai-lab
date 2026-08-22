"""
Document Loaders + Text Splitters
Goal: Load a document and split it into manageable chunks
so they can be indexed later.
"""

from dotenv import load_dotenv
import os

load_dotenv()
RAG_DATA_PATH = os.getenv('RAG_DATA_PATH')
PDF_FILENAME = "lideres_nba_25-26.pdf"

# We've chosen PyPDF but there is PyMuPDFLoader, UnstructuredPDFLoader, etc.
from langchain_community.document_loaders import PyPDFLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_PDF():
    splits = None
    # Uploading PDF with PDF path
    loader = PyPDFLoader(f"{RAG_DATA_PATH}/{PDF_FILENAME}")
    documentos = loader.load()

    if len(documentos): # Quick simple validation, insufficient to prod env obviosuly

        print("*****************")
        print(f"Ingesting document '{PDF_FILENAME}' to enrich AI prompts (RAG architecture)")
        print("*****************")

        print(f"Uploaded document with {len(documentos)} pages")

        # Split the document into smaller chunks to avoid issues caused by LLM context limits,
        # and because searching smaller chunks is more precise than searching the entire document
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=300, # split on 300 characters blocks
            chunk_overlap=100, # 50 characters of margin
            length_function=len, # Is len by default, only set-up to learn it. Can be token with custom function to be more efficient.
            is_separator_regex=False, # Is False by default, only set-up to learn it
        )

        splits = splitter.split_documents(documentos)

        print(f"Document split in {len(splits)} parts")
        print("")

    else: 
        print(f"Error splitting document")
        print("")

    return splits