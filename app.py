import streamlit as st
import os
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq 
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.prompt import system_prompt

# 1. Page Configuration
st.set_page_config(page_title="MediQuery.ai", page_icon="🏥")
st.title("🏥 MediQuery.ai: Medical Assistant")

# 2. Load Environment Variables (Using st.secrets for Cloud)
PINECONE_API_KEY = st.secrets.get("PINECONE_API_KEY")
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY")

if not PINECONE_API_KEY or not GROQ_API_KEY:
    st.error("API Keys not found! Please add them to Streamlit Secrets.")
    st.stop()

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

# 3. Cache Core Components (Prevents reloading on every interaction)
@st.cache_resource
def init_rag():
    embeddings = download_hugging_face_embeddings()
    index_name = "medical-chatbot" 

    docsearch = PineconeVectorStore.from_existing_index(
        index_name=index_name,
        embedding=embeddings
    )

    retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

    chatModel = ChatGroq(
        model="llama-3.3-70b-versatile", 
        groq_api_key=GROQ_API_KEY,
        temperature=0.4
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
    return create_retrieval_chain(retriever, question_answer_chain)

rag_chain = init_rag()

# 4. Chat History Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display Chat Interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. User Input Logic
if prompt := st.chat_input("How can I help you today?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate RAG Response
    with st.chat_message("assistant"):
        with st.spinner("Consulting medical database..."):
            response = rag_chain.invoke({"input": prompt})
            answer = response["answer"]
            st.markdown(answer)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": answer})
