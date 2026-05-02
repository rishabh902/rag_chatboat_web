Debales AI Assistant

This project is an AI-powered chatbot built to intelligently answer user queries by combining Retrieval-Augmented Generation (RAG) and external search (SERP API) within a LangGraph workflow.

The system first analyzes the user’s question and decides the best way to respond:

For Debales AI–related queries, it uses RAG, retrieving information from a locally stored knowledge base created by scraping Debales AI website data and storing it in a FAISS vector database.
For general or real-time queries, it uses a SERP API (Tavily) to fetch relevant information from the internet.
For mixed queries, it combines both sources to generate a complete and accurate response.



Key Features
Intelligent routing (RAG vs SERP vs Both)
Vector-based semantic search using FAISS
Real-time data retrieval using Tavily API
LLM-powered response generation using Groq
No hallucination (safe fallback responses)
Clean and interactive UI with FastAPI



Tech Stack
Python
LangChain
LangGraph
FAISS
HuggingFace Embeddings
Groq API
Tavily API
FastAPI
