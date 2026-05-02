import streamlit as st
import os
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq 
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.prompt import system_prompt

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="MediQuery.ai", page_icon="🏥", layout="centered")
st.title("🏥 MediQuery.ai: Medical Assistant")
st.markdown("---")

# --- LOAD SECRETS ---
# Streamlit Cloud uses st.secrets to pull keys from the 'Secrets' menu
PINECONE_API_KEY = st.secrets.get("PINECONE_API_KEY")
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")

if not PINECONE_API_KEY or not GROQ_API_KEY:
    st.error("Missing API Keys! Please add PINECONE_API_KEY and GROQ_API_KEY to Streamlit Secrets.")
    st.stop()

# Set environment variable for internal LangChain/Pinecone tools
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

# --- INITIALIZE RAG COMPONENTS (CACHED) ---
@st.cache_resource
def init_rag():
    # Load Embeddings
    embeddings = download_hugging_face_embeddings()
    index_name = "medical-chatbot" 

    # Connect to Pinecone
    docsearch = PineconeVectorStore.from_existing_index(
        index_name=index_name,
        embedding=embeddings
    )

    retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    # Initialize LLM
    chat_model = ChatGroq(
        model="llama-3.3-70b-versatile", 
        groq_api_key=GROQ_API_KEY,
        temperature=0.4
    )

    # Setup RAG Chain
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(chat_model, prompt_template)
    return create_retrieval_chain(retriever, question_answer_chain)

# Load the chain once and keep it in memory
rag_chain = init_rag()

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if user_query := st.chat_input("How can I help you today?"):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Generate Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Searching medical records..."):
            try:
                response = rag_chain.invoke({"input": user_query})
                full_response = response["answer"]
                st.markdown(full_response)
                # Store assistant response
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
