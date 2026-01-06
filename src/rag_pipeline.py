from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import List, Dict
from .models import AnswerSource
from .vector_store import search_documents
from .tavily_integration import search_web
import os

def assemble_context(query: str, classification: str, vectorstore, top_k: int = 5) -> str:
    context_parts = []
    sources = []

    if classification in ['document', 'hybrid']:
        docs = search_documents(query, vectorstore, top_k)
        for doc in docs:
            context_parts.append(f"[Doc] {doc.metadata['title']} - Chunk {doc.metadata['chunk_index']}: {doc.page_content}")
            sources.append(AnswerSource(
                source_type="document",
                title=doc.metadata['title'],
                citation=f"[Doc] {doc.metadata['title']} – Chunk {doc.metadata['chunk_index']}",
                content=doc.page_content
            ))

    if classification in ['web', 'hybrid']:
        web_results = search_web(query)
        for result in web_results[:top_k]:
            context_parts.append(f"[Web] {result.title}: {result.content}")
            sources.append(AnswerSource(
                source_type="web",
                title=result.title,
                citation=f"[Web] Tavily: \"{result.title}\"",
                content=result.content
            ))

    context = "\n\n".join(context_parts)
    return context, sources

def generate_answer(query: str, context: str) -> str:
    # For demo purposes, return a simple answer based on context without API calls
    if context:
        return f"Based on the documents: {context[:500]}... (Demo mode - no LLM used)"
    else:
        return "No relevant information found in documents. (Demo mode)"

def get_top_summaries(sources: List[AnswerSource], top_n: int = 3) -> List[str]:
    # Simple summary: just the content truncated
    summaries = []
    for source in sources[:top_n]:
        summary = source.content[:200] + "..." if len(source.content) > 200 else source.content
        summaries.append(f"{source.citation}: {summary}")
    return summaries