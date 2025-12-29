from langchain_text_splitters import RecursiveCharacterTextSplitter

code_splitter = RecursiveCharacterTextSplitter.from_language(language = 'python',
                                chunk_size = 500, chunk_overlap = 100)

with open("dummy_code.py", 'r') as file:
    raw_text = file.read()

# print("Raw Text: ", raw_text)
docs = code_splitter.create_documents([raw_text])

#i = 1
#for doc in docs:
#   print(f" chunk_{i}--->> {doc.page_content}")
#   i=i+1
#   print("\n\n")

print(docs[0])
print("\n\n")
print(docs[1])
print("\n\n")
print(docs[2])