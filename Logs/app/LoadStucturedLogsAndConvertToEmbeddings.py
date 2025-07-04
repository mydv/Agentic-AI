import json
import faiss
import pandas as pd
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

# Load log lines
logs = []
with open("logs/structured_logs_timestamp.jsonl", "r") as f:
    for line in f:
        logs.append(json.loads(line))

# Choose what to embed
texts = [log["message"] for log in logs]

# Load embedding model (MiniLM is fast and accurate)
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(texts, show_progress_bar=True)

# Store in DataFrame for reference
df = pd.DataFrame(logs)
df["embedding"] = embeddings.tolist()

#Build and Store Faiss Index
# Convert to float32 for FAISS
embeddings_np = np.array(embeddings).astype("float32")

# Create a FAISS index
index = faiss.IndexFlatL2(embeddings_np.shape[1])
index.add(embeddings_np)

# Save the index
faiss.write_index(index, "faiss/faiss_log_index.idx")

# Optionally save metadata for reverse lookup
df.to_json("faiss/faiss_log_metadata.jsonl", orient="records", lines=True)

#Perform a similarity search on new incidents
def search_similar_logs(query_text, top_k=3):
    query_vec = model.encode([query_text]).astype("float32")
    D, I = index.search(query_vec, top_k)
    return df.iloc[I[0]]

# Example
result = search_similar_logs("payment failed due to gateway issue")
print(result[["timestamp", "user_id", "message"]])