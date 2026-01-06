# Multi-Document RAG Search Engine with Real-Time Web Search

This project implements a hybrid RAG (Retrieval-Augmented Generation) system that combines multi-document semantic search with real-time web search using Tavily.


## Features

- Multi-source document ingestion (PDFs, Wikipedia, Text files)
- FAISS vector indexing for semantic search
- Tavily integration for real-time web search (disabled in demo)
- Query classification (defaults to document search in demo)
- Streamlit-based chatbot UI with source citations
- Cost-free demo operation

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. For full functionality (optional), create a `.env` file with API keys:
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
2. Load Wikipedia pages (requires internet)
3. Ask questions - the system searches your documents and returns relevant information
4. View source citations and evidence tabs

## Architecture

- **Ingestion**: Load and normalize documents from various sources
- **Chunking**: Split documents into overlapping chunks
- **Vector Store**: FAISS for efficient semantic search
- **RAG Pipeline**: Assemble context and generate answers 
- **UI**: Streamlit interface for interaction
