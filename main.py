from app.graph import build_graph
from fastapi import FastAPI


app = build_graph()

print("Debales AI Assistant Started")


while True:
    question = input("Ask question: ")

    if question.lower() == "exit":
        break

    result = app.invoke({
        "question": question,
        "route": "",
        "rag_result": "",
        "serp_result": "",
        "final_answer": ""
    })

    print("\nAnswer:")
    print(result["final_answer"])
   