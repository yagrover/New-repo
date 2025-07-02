from sentence_transformers import SentenceTransformer
import faiss
import os
import pickle

# Load embedding model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def load_documents_from_folder(folder_path):
    documents = []
    filenames = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), "r", encoding="utf-8") as f:
                text = f.read()
                documents.append(text)
                filenames.append(filename)
    return documents, filenames

def build_faiss_index(documents):
    embeddings = embedding_model.encode(documents)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, embeddings

def save_faiss_index(index, documents, file_path="faiss_store"):
    faiss.write_index(index, file_path + ".index")
    with open(file_path + ".meta", "wb") as f:
        pickle.dump(documents, f)

def load_faiss_index(file_path="faiss_store"):
    index = faiss.read_index(file_path + ".index")
    with open(file_path + ".meta", "rb") as f:
        docs = pickle.load(f)
    return index, docs

def query_faiss(query, index, documents, k=2):
    query_embedding = embedding_model.encode([query])
    D, I = index.search(query_embedding, k)
    return [documents[i] for i in I[0]]
