from typing import TypedDict  # we will define fixed schema for dictionry
from langgraph.graph import StateGraph, END  # create graph/flow
from langchain_groq import ChatGroq  #Used to connect Groq LLM model. this provide free api key 
from dotenv import load_dotenv # we have create env file so we load botenv

from app.rag import rag_answer  #import other file 
from app.serp_tool import serp_answer 

load_dotenv()


class AgentState(TypedDict):  #thsi is memory pass graph node all 
    question: str
    route: str
    rag_result: str
    serp_result: str
    final_answer: str

 #creating graph model llm objects 
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0  # Temperature we can set stable , and low and hight output. 
                    # we can set range  temperature 0-2 only  
)


def node_path(state: AgentState):  #beacuse we have 2 path rag and google api serp 

    question = state["question"].lower() #all question should be in lowercase


    #These are keywords related to Debales ai.If user question contains thses words, we assume it is related to Debales.
    debales_words = ["debales", "logistics", "freight", "3pl", "automation", "tms", "wms"]

    #These words use mean current information is needed.
    external_words = ["latest", "news", "current", "today", "compare", "competitor"]

    is_debales = any(word in question for word in debales_words) #we are checkinh debles keyword is exits or not
    is_external = any(word in question for word in external_words)

    # if keyword match we wil pass the path and return the result

    if is_debales and is_external:
        route = "both"
    elif is_debales:
        route = "rag"
    else:
        route = "serp"

    return {"route": route}


def rag_node(state: AgentState): #this rag handle debales ai related question 
    return {"rag_result": rag_answer(state["question"])}


def serp_node(state: AgentState): #this serp function handle goggle search 
    return {"serp_result": serp_answer(state["question"])} 
 #for serp we have use Tavily api key 

# create a prompt for templete , we will check state and pass answer 
def final_node(state: AgentState):
    prompt = f"""
Create a clear final answer.

Question:
{state["question"]}

Debales RAG Answer:
{state.get("rag_result", "")}

SERP Answer:
{state.get("serp_result", "")}

"""

    response = llm.invoke(prompt)  # this prompt groq model , retrnn the response and store all answers , 
    return {"final_answer": response.content}


def route_decision(state: AgentState):
    return state["route"]


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", node_path)
    graph.add_node("rag", rag_node)
    graph.add_node("serp", serp_node)
    graph.add_node("final", final_node)


# This is routing logic.
    graph.set_entry_point("router")



    graph.add_conditional_edges(
        "router",
        route_decision,
        {
            "rag": "rag",
            "serp": "serp",
            "both": "rag"
        }
    )

    graph.add_conditional_edges(
        "rag",
        lambda state: "serp" if state["route"] == "both" else "final",
        {
            "serp": "serp",
            "final": "final"
        }
    )

    graph.add_edge("serp", "final")
    graph.add_edge("final", END)

    return graph.compile()