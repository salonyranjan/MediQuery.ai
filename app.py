from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq 
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os

# 1. Initialize App and Load Environment
app = Flask(__name__)
load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

# Ensure keys are set as environment variables for LangChain tools
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

# 2. Load Core Components
embeddings = download_hugging_face_embeddings()
index_name = "medical-chatbot" 

# Connect to Pinecone
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

# 3. Setup LLM (Groq)
chatModel = ChatGroq(
    model="llama-3.3-70b-versatile", 
    groq_api_key=GROQ_API_KEY,
    temperature=0.4
)

# 4. Setup RAG Chain
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# 5. Routes
@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form.get("msg")
    if not msg:
        return "Please enter a message."
        
    print(f"User Input: {msg}")
    
    # Process through RAG
    response = rag_chain.invoke({"input": msg})
    
    print("Response : ", response["answer"])
    return str(response["answer"])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)