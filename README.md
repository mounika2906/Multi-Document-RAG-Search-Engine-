# Multi-Document RAG Search Engine with Real-Time Web Search

This project implements a hybrid RAG (Retrieval-Augmented Generation) system that combines multi-document semantic search with real-time web search using Tavily.

## Features

- Multi-source document ingestion (PDFs, Wikipedia, Text files)
- FAISS vector indexing for semantic search
- Tavily integration for real-time web search
- Query classification for routing between document and web sources
- Streamlit-based chatbot UI with source citations

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   Create a `.env` file with:
   ```
   OPENAI_API_KEY=your_openai_key
   TAVILY_API_KEY=your_tavily_key
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Upload documents via the sidebar
2. Load Wikipedia pages if needed
3. Ask questions in the chat interface
4. View answers with citations and evidence tabs

## Architecture

- **Ingestion**: Load and normalize documents from various sources
- **Chunking**: Split documents into overlapping chunks
- **Vector Store**: FAISS for efficient semantic search
- **Query Classification**: Route queries to appropriate sources
- **RAG Pipeline**: Assemble context and generate answers with citations
- **UI**: Streamlit interface for interaction