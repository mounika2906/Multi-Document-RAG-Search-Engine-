from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from .models import Document, DocumentChunk

def chunk_documents(docs: List[Document], chunk_size: int = 1000, overlap: int = 200) -> List[DocumentChunk]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = []
    for doc in docs:
        lang_docs = splitter.create_documents([doc.content], metadatas=[doc.metadata])
        for i, lang_doc in enumerate(lang_docs):
            chunk = DocumentChunk(
                source_id=doc.source_id,
                source_type=doc.source_type,
                title=doc.title,
                content=lang_doc.page_content,
                chunk_index=i,
                metadata={**lang_doc.metadata, "chunk_index": i}
            )
            chunks.append(chunk)
    return chunks