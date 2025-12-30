from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import chromadb

# Load the PDF 
path = r"D:\Intrenship\94460-GenAI-Assignments\Day 08\resume-003.pdf"

loader = PyPDFLoader(path)
docs = loader.load()

#Chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 400,
    chunk_overlap=40
) # Definig the Cunk size and overlap 

chunks = splitter.split_documents(docs) #Splits the document 
chunk_texts=[ c.page_content for c in chunks ] # stores into the chunk_texts

# creating the Embeddings 
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

embedding = embedding_model.embed_documents(chunk_texts)

# Init Croma 
client = chromadb.Client(
    settings=chromadb.Settings(persist_directory = "./resume_db")
)
# Starting the Cromadb and setting the foldeer name = reume_db
collection = client.get_or_create_collection(name="resume")
#Creating and loading the table name called resume


# Building the Id's and metadata
ids = [ f"resume_{i}" for i in range(len(chunk_texts))]

metadata = [
    {
        "page":chunks[i].metadata.get("page")
    }for i in range(len(chunks))
]

#insert 

collection.add(
    ids = ids ,
    documents=chunk_texts,
    embeddings=embedding,
    metadatas=metadata
)

# client.persist()
print("\n💾 DONE: Resume stored in vector DB.\n")


#Now test the query 
query = "What skills does the candidate have ? "
query_embed=embedding_model.embed_query(query)

results= collection.query(
    query_embeddings=[query_embed],
    n_results=2
)

#printing the query results 
for doc,meta,dist in zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0]
):
    print(f"Page: {meta['page']}  |  Distance: {dist}")
    print(doc)
    print("----")