import faiss
import json
import pandas as pd

# Load FAISS index and metadata
faiss_index = faiss.read_index("faiss_log_index.idx")
df_logs = pd.read_json("faiss_log_metadata.jsonl", lines=True)

#Create the embedding model
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(text):
    return embedding_model.encode([text])[0].astype("float32")

#Define a search function on FAISS

def search_logs(query, top_k=5):
    query_vec = embed(query)
    D, I = faiss_index.search(query_vec.reshape(1, -1), top_k)
    return df_logs.iloc[I[0]].to_dict(orient="records")


#Construct the langchain agent
	
from langchain_community.llms import Ollama
from langchain.schema import SystemMessage, HumanMessage

llm = Ollama(model="mistral")

def analyze_logs(query):
    similar_logs = search_logs(query)
    context = "\n".join([f"{log['timestamp']} | {log['level']} | {log['user_id']} | {log['message']}" for log in similar_logs])

    messages = [
        SystemMessage(content="You are an AI incident responder. Analyze log errors and suggest probable causes or fixes."),
        HumanMessage(content=f"Logs:\n{context}\n\nQuery:\n{query}\n\nWhat is the most likely root cause and how should we resolve this?")
    ]

    return llm.invoke(messages)
	
#Run it
query = "payment failed due to gateway timeout"
response = analyze_logs(query)
print("🔍 Root Cause Analysis:\n", response)