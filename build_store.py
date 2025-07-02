from rag_utils import load_documents_from_folder, build_faiss_index, save_faiss_index

# Load .txt documents
docs, filenames = load_documents_from_folder("data")

# Build FAISS index
index, _ = build_faiss_index(docs)

# Save index and filenames
save_faiss_index(index, docs, file_path="faiss_store")

print("✅ FAISS store created and saved.")
