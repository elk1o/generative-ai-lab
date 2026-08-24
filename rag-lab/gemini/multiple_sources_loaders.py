"""
Document Loaders + Text Splitters — multi-document version
Goal: load multiple PDFs, split them into chunks, and prepare them for joint indexing.
"""
from dotenv import load_dotenv
import os
# We've chosen PyPDF but there is PyMuPDFLoader, UnstructuredPDFLoader, etc.
from langchain_community.document_loaders import PyPDFLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()
RAG_DATA_PATH = os.getenv('RAG_DATA_PATH')
PDF_FILENAME = "lideres_nba_25-26.pdf"
PDF_FILENAME_AUX = 'triples_dobles_sports_illustrated.pdf'

pdfs_path = [
    f"{RAG_DATA_PATH}/{PDF_FILENAME}",
    f"{RAG_DATA_PATH}/{PDF_FILENAME_AUX}",
]

def load_multiple_PDFs():
    print("*****************")
    print(f"Splitting documents {str(pdfs_path)}")
    print("*****************")
    
    documents = []
    for pdf in pdfs_path:
        loader = PyPDFLoader(pdf)
        uploaded_document = loader.load()
        documents.extend(uploaded_document)
        print(f"Uploaded: {pdf} → {len(uploaded_document)} página(s)")

    print(f"Total pages uploaded on documents: {len(documents)}")

    # Uploading PDF with PDF path

    if len(documents): # Quick simple validation, insufficient to prod env obviosuly

        print(f"Ingesting documents")
        print(f"Uploaded document with {len(documents)} pages")

        # Split the document into smaller chunks to avoid issues caused by LLM context limits,
        # and because searching smaller chunks is more precise than searching the entire document
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=300, # split on 300 characters blocks
            chunk_overlap=100, # 50 characters of margin
            length_function=len, # Is len by default, only set-up to learn it. Can be token with custom function to be more efficient.
            is_separator_regex=False, # Is False by default, only set-up to learn it
        )

        splits = splitter.split_documents(documents)

        print(f"Document split in {len(splits)} chunks")
        print("")

    else: 
        print(f"Error splitting document")
        print("")

    return splits