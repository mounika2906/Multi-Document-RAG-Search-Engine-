from langchain.vectorstores import FAISS
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.schema import Document as LangDocument
from typing import List
from .models import DocumentChunk
import os

def index_documents(chunks: List[DocumentChunk], index_path: str = "faiss_index"):
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    lang_docs = [
        LangDocument(
            page_content=chunk.content,
            metadata={
                "source_id": chunk.source_id,
                "source_type": chunk.source_type,
                "title": chunk.title,
                "chunk_index": chunk.chunk_index,
                **chunk.metadata
            }
        ) for chunk in chunks
    ]
    vectorstore = FAISS.from_documents(lang_docs, embeddings)
    vectorstore.save_local(index_path)
    return vectorstore

def load_faiss_index(index_path: str = "faiss_index"):
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(index_path, embeddings)
    return vectorstore

def search_documents(query: str, vectorstore, top_k: int = 5):
    docs = vectorstore.similarity_search(query, k=top_k)
    return docs