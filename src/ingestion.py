from langchain_community.document_loaders import PyPDFLoader, WikipediaLoader, TextLoader
from langchain.schema import Document as LangDocument
from typing import List
from .models import Document
import os

def load_pdf(file_path: str) -> List[Document]:
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    return [
        Document(
            source_id=file_path,
            source_type="pdf",
            title=os.path.basename(file_path),
            content=doc.page_content,
            metadata=doc.metadata
        ) for doc in docs
    ]

def load_wikipedia(query: str) -> List[Document]:
    loader = WikipediaLoader(query=query, load_max_docs=5)
    docs = loader.load()
    return [
        Document(
            source_id=f"wikipedia:{query}",
            source_type="wikipedia",
            title=doc.metadata.get("title", query),
            content=doc.page_content,
            metadata=doc.metadata
        ) for doc in docs
    ]

def load_text(file_path: str) -> List[Document]:
    loader = TextLoader(file_path)
    docs = loader.load()
    return [
        Document(
            source_id=file_path,
            source_type="text",
            title=os.path.basename(file_path),
            content=doc.page_content,
            metadata=doc.metadata
        ) for doc in docs
    ]

def clean_text(text: str) -> str:
    # Basic cleaning: remove extra whitespaces, normalize
    import re
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def normalize_documents(docs: List[Document]) -> List[Document]:
    for doc in docs:
        doc.content = clean_text(doc.content)
    return docs