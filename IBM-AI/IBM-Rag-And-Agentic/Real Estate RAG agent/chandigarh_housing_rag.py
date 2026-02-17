import os
from dotenv import load_dotenv

for proxy_var in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"]:
    os.environ.pop(proxy_var, None)

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Please set your GOOGLE_API_KEY in the .env file!")

from langchain_community.document_loaders import PyPDFLoader

print("Step1: Loading the PDF file")
loader = PyPDFLoader("CHB-Brochure-5.7.23.pdf")
documents = loader.load()
print(f"Loaded {len(documents)} pages from the CHB housing PDF.")

from langchain.text_splitter import RecursiveCharacterTextSplitter

# Make the chunks

print("Step2: Splitting the documents into chunks")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50,
    separators=["\n\n", "\n", " ", ""]
)
chunks = text_splitter.split_documents(documents)
print(f" Created {len(chunks)} chunks from the PDF of {len(documents)} pages.")

# Embedding + Storing 
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

print("Step3: Creating the embeddings and storing in ChromaDB")
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=GOOGLE_API_KEY
)

vector_store = Chroma.from_documents(
    chunks,
    embedding_model,
    persist_directory="./chroma_chb_housing"
)

print(f"Stored {len(chunks)} chunks in ChromaDB.")

# Creating the rag chain 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# from renumics import spotlight
# import pandas as pd
# import numpy as np

# print("Step 4: Preparing 3D Visualization...")

# # 1. ChromaDB se data nikaalo
# data = vector_store.get(include=['embeddings', 'documents', 'metadatas'])

# # 2. Embeddings ko NumPy array mein convert karo taaki Pandas gussa na kare
# # Hum har embedding ko ek individual array banayenge
# embeddings_list = [np.array(e) for e in data['embeddings']]

# # 3. DataFrame banao
# df = pd.DataFrame({
#     "text": data['documents'],
#     "embedding": embeddings_list,
#     "metadata": [str(m) for m in data['metadatas']]
# })

# print(f"Visualizing {len(df)} points in 3D...")

# # 4. Spotlight launch karo
# # Browser mein "Similarity Map" par click karna 3D ke liye
# spotlight.show(df)

llm = ChatGoogleGenerativeAI(
    model = "gemini-2.0-flash",
    google_api_key = GOOGLE_API_KEY,
    max_output_tokens = 1024,
    temperature = 0.3
)

retriever = vector_store.as_retriever(search_kwargs={"k": 4})

rag_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant specializing in Chandigarh Housing Board (CHB) schemes. 
Answer questions ONLY based on the provided context from the CHB brochure. 
If the context doesn't contain the answer, say "This information is not available in the CHB brochure."
Be specific with numbers, dates, eligibility criteria, and prices when available."""),
    ("human", """Context from CHB Brochure:
{context}

Question: {question}

Answer:""")
])

def format_docs(docs):
    return "\n\n---\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context":retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm 
    | StrOutputParser()
)

# ============================================================
# Step 5: INTERACTIVE CHAT LOOP
# ============================================================
print("\n" + "=" * 60)
print("  CHB HOUSING SCHEME - RAG Assistant")
print("  Ask anything about the Chandigarh Housing Board scheme.")
print("  Type 'quit' to exit.")
print("=" * 60)

while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ["quit", "exit", "bye"]:
        print("Ending chat. Goodbye!")
        break
    response = rag_chain.invoke(user_input)
    print(f"AI: {response}")
