from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI

MODEL = "gemini-3.5-flash-lite"

# ========================================================
# State
# ========================================================

class State(TypedDict):
    product_text: str
    product_info: str
    marketing_text: str
    final_description: str

# ========================================================
# Nodes
# ========================================================

def extract(state: State) -> State:
    llm = ChatGoogleGenerativeAI(
        model=MODEL
    )

    prompt = f"""
    You are a product information extraction model.
    Extract the main product information from the following text:
    {state['product_text']}
    Return only the extracted information in the format:
    Product: ...
    Display: ...
    Storage: ...
    Processor: ...
    Camera: ...
    Connector: ...
    Colors: ...
    """

    response = llm.invoke(prompt)

    return {
        "product_info": response.text
    }

def marketing(state: State) -> State:
    llm = ChatGoogleGenerativeAI(
        model=MODEL
    )

    prompt = f"""
    You are a marketing text generation model.
    Create a marketing text based on the following product information:
    {state['product_info']}
    Return only the marketing text.
    """

    response = llm.invoke(prompt)

    return {
        "marketing_text": response.text
    }

def format(state: State) -> State:
    final_description = f"""
    === PRODUCT DESCRIPTION ===

    {state['marketing_text']}

    === END ===
    """

    return {
        "final_description": final_description
    }

# ========================================================
# Graph
# ========================================================

builder = StateGraph(State)

builder.add_node("extract", extract)
builder.add_node("marketing", marketing)
builder.add_node("format", format)

builder.add_edge(START, "extract")
builder.add_edge("extract", "marketing")
builder.add_edge("marketing", "format")
builder.add_edge("format", END)

graph = builder.compile()

result = graph.invoke({
    "product_text": "iphone 15, 6.1 inch oled, 128gb, a16 bionic, 48mp camera, usb-c, battery good, available in black and blue",
    "product_info": "",
    "marketing_text": "",
    "final_description": ""
})

print("Final description:", result.get("final_description"))


