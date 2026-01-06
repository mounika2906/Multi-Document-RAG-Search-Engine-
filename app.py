import streamlit as st
from src.ingestion import load_pdf, load_wikipedia, load_text, normalize_documents
from src.chunking import chunk_documents
from src.vector_store import index_documents, load_faiss_index
from src.query_classification import classify_query
from src.rag_pipeline import assemble_context, generate_answer, get_top_summaries
from src.tavily_integration import search_web
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Multi-Document RAG Search Engine", layout="wide")

# Sidebar for document management
st.sidebar.title("Document Management")
uploaded_files = st.sidebar.file_uploader("Upload PDFs or Text Files", accept_multiple_files=True, type=['pdf', 'txt'])
wikipedia_query = st.sidebar.text_input("Wikipedia Query")
if st.sidebar.button("Load Documents"):
    try:
        docs = []
        for file in uploaded_files:
            if file.type == "application/pdf":
                # Save temp and load
                with open(f"temp_{file.name}", "wb") as f:
                    f.write(file.getbuffer())
                docs.extend(load_pdf(f"temp_{file.name}"))
                os.remove(f"temp_{file.name}")
            elif file.type == "text/plain":
                content = file.getvalue().decode("utf-8")
                from src.models import Document
                docs.append(Document(
                    source_id=file.name,
                    source_type="text",
                    title=file.name,
                    content=content,
                    metadata={}
                ))
        if wikipedia_query:
            docs.extend(load_wikipedia(wikipedia_query))
        docs = normalize_documents(docs)
        chunks = chunk_documents(docs)
        vectorstore = index_documents(chunks, "faiss_index")
        st.sidebar.success("Documents indexed!")
    except Exception as e:
        st.sidebar.error(f"Error loading documents: {str(e)}")

tavily_enabled = st.sidebar.checkbox("Enable Tavily Web Search", value=True)

# Main chat interface
st.title("Hybrid RAG Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            vectorstore = load_faiss_index("faiss_index")
            classification = classify_query(prompt)
            context, sources = assemble_context(prompt, classification, vectorstore)
            answer = generate_answer(prompt, context)
            summaries = get_top_summaries(sources)

            # Display answer
            st.markdown(answer)

            # Tabs for evidence
            tab1, tab2, tab3 = st.tabs(["Answer", "Document Evidence", "Web Evidence"])
            with tab1:
                st.markdown(answer)
            with tab2:
                doc_sources = [s for s in sources if s.source_type == "document"]
                for s in doc_sources:
                    st.markdown(f"**{s.citation}**")
                    st.markdown(s.content[:500] + "...")
            with tab3:
                web_sources = [s for s in sources if s.source_type == "web"]
                for s in web_sources:
                    st.markdown(f"**{s.citation}**")
                    st.markdown(s.content[:500] + "...")

            # Indicator
            if classification == "document":
                st.markdown("📄 Document-based answer")
            elif classification == "web":
                st.markdown("🌐 Web-based answer")
            else:
                st.markdown("🔀 Hybrid answer")

            st.session_state.messages.append({"role": "assistant", "content": answer})

        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.session_state.messages.append({"role": "assistant", "content": f"Error: {str(e)}"})