from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles

from app.graph import build_graph

app = FastAPI()

templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")

graph_app = build_graph()

#we have two end point 
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "answer": None,
            "question": None
        }
    )


@app.post("/generate", response_class=HTMLResponse)
def ask_question(request: Request, question: str = Form(...)):
    result = graph_app.invoke({
        "question": question,
        "route": "",
        "rag_result": "",
        "serp_result": "",
        "final_answer": ""
    })

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "answer": result["final_answer"],
            "question": question
        }
    )