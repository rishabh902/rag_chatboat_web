from langchain_community.vectorstores import FAISS  #FAISS = Vector convert in vector formate 

from langchain_huggingface import HuggingFaceEmbeddings  #convert text to vector (number ) , becsaus maching can untersand only numbers 

from langchain_text_splitters import RecursiveCharacterTextSplitter #we have use langchaain  textesplitter 
# from langchain.schema import Document
#we use this for text wrap
from langchain_core.documents import Document  


def create_vectors(): #create function and read  all text from scraper  folder 
    with open("data/debales_scraper.txt", "r", encoding="utf-8") as file:  # only read mode 
        text = file.read()

    docs = [Document(page_content=text)] 
    # Converts raw text into LangChain Document and split all text 

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    ).split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )

    FAISS.from_documents(chunks, embeddings).save_local("vectorstore")

    print("Vectorstore created successfully")


if __name__ == "__main__":
    create_vectors()