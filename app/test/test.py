from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

db = Chroma(
    persist_directory="back_chatbot_v2/data/vector_db_unificado",
    embedding_function=emb,
    collection_name="orfeo_codigo"
)

# results = db.get(
#     where={"file": {"$eq": "ver_historico.php"}}
# )

# print(len(results["documents"]))

data = db.get()

print("Keys:", data.keys())
print("Total docs:", len(data["documents"]))
print("Total metadatas:", len(data["metadatas"]))

# imprime los primeros 3 completos
for i in range(min(3, len(data["metadatas"]))):
    print("----")
    print(data["metadatas"][i])