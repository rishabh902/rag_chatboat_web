from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS  # FAISS = Vector convert in vector formate
from langchain_huggingface import HuggingFaceEmbeddings  # convert text to vector (number), because machine can understand only numbers
from langchain_groq import ChatGroq  # for groq api key

load_dotenv()

# create one this for better performance
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2
)


def rag_answer(question):
    #load vector database
    vectorstore = FAISS.load_local(
        "vectorstore",
        embeddings,
        allow_dangerous_deserialization=True
    )

    #search similar chunks
    docs = vectorstore.similarity_search(question, k=3)

    #combine context and load page
    context = "\n\n".join(doc.page_content for doc in docs)

    # prompt for LLM
    prompt = f"""
You are Debales AI assistant.

Answer only using the given context.
If answer is not available, say: "I don't know based on Debales AI data."

Context:
{context}

Question:
{question}
"""

    # get response
    return llm.invoke(prompt).content