from langchain_huggingface import HuggingFaceEmbeddings
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader


path = r"D:\Intrenship\94460-GenAI-Assignments\Day 08\Resumes"

loader= DirectoryLoader(
    path,
    glob="**/*.pdf",
    loader_cls=PyPDFLoader
)

docs  = loader.load()

# Chunks 
Splitter= RecursiveCharacterTextSplitter(
    chunk_size = 784,
    chunk_overlap =100
)
chunks = Splitter.split_documents(docs)
chunks_text = [ c.page_content for c in chunks]

# Embedding model 
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

embeddings = embedding_model.embed_documents(chunks_text)

# Init Croma
# client = chromadb.Client(
#     settings=chromadb.Settings(persist_directory = "./outputs")
# )
client = chromadb.PersistentClient(path=r"D:\Intrenship\94460-GenAI-Assignments\Day 08\outputs")
print(client)

collection = client.get_or_create_collection("resume_col")


#Biulding the ids and the meta-data
ids = [ f"resume_{i}" for i in range(len(chunks))]

metadata = [
    {
        "page":chunks[i].metadata.get("page")
    }for i in range(len(chunks))
]

#insert 
collection.add(
    ids=ids,
    metadatas=metadata,
    embeddings=embeddings,
    documents=chunks_text   
)
#client.persist()    

print(" ✅ The Resumnes are get stored in the vector db ")

while True:

    #Now test gthe query 
    query = input("Hi HR -> Enter query you want  :  ")

    if query == "exit":
        break

    query_embed = embedding_model.embed_query(query)
    k = int(input("Enter how many outputs you want ? :"))
    results = collection.query(
        query_embeddings=[query_embed],
        n_results=k
    )

    #printing the results

    for doc,meta,dis in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        print(f" Page : {meta} -> dist : {dis}")
        print("text :",doc)
        print("--------------------------------------------------")

print("Thank You 😊")