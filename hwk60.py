# Multi-Agent Travel Planner

from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage

# ==============================================================
# State
# ==============================================================

class State(TypedDict):
    user_request: str
    destination_info: str
    food_info: str
    budget_info: str
    final_plan: str

# ==============================================================
# Model
# ==============================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite"
)

# ==============================================================
# Output Schema
# ==============================================================

class BudgetResult(BaseModel):
    currency: str = Field(..., description="Currency code, e.g. EUR")
    accommodation: float = Field(..., description="Total accommodation cost for the whole trip")
    food: float = Field(..., description="Total food cost for the whole trip")
    transportation: float = Field(..., description="Total local and arrival transport cost")
    activities: float = Field(..., description="Total cost of tickets and activities")
    total: float = Field(..., description="Sum of all categories")
    notes: str = Field(..., description="Short assumptions behind the estimate")

budget_llm = llm.with_structured_output(BudgetResult)

# ==============================================================
# Destination Agent
# ==============================================================

def destination_agent(state: State) -> dict:
    user_request = state["user_request"]

    prompt = [
        SystemMessage(
            content="""
            You are a destination specialist.
            Your ONLY job: analyze the destination in the user's request, decide which
            types of activities fit the user's interests, and recommend specific places/activities.
            Do NOT discuss food, restaurants, or costs.
            """
        ),
        HumanMessage(
            content=f"User request: {user_request}"
        )
    ]

    response = llm.invoke(prompt)
    return {
        "destination_info": response.text
    }

# ==============================================================
# Food Agent
# ==============================================================

def food_agent(state: State) -> dict:
    user_request = state["user_request"]

    prompt = [
        SystemMessage(
            content="""
            You are a food specialist.
            Your ONLY job: recommend local dishes, restaurants, markets and food experiences
            for the destination in the user's request, matching their tastes and budget level.
            Do NOT plan the itinerary, sightseeing, or calculate the total trip budget.
            """
        ),
        HumanMessage(
            content=f"User request: {user_request}"
        )
    ]

    response = llm.invoke(prompt)
    return {
        "food_info": response.text
    }

# ==============================================================
# Budget Agent
# ==============================================================

def budget_agent(state: State) -> dict:
    user_request = state["user_request"]

    prompt = [
        SystemMessage(
            content="""
            You are a travel budget analyst.
            Your ONLY job is estimating costs for the trip described by the user.
            Consider trip length, destination prices, and the user's budget level.
            Split costs into: accommodation, food, transportation, activities.
            Do NOT recommend specific attractions or restaurants.
            """
        ),
        HumanMessage(
            content=f"User request: {user_request}"
        )
    ]

    r = budget_llm.invoke(prompt)
    budget_text = (
        f"Accommodation: {r.accommodation} {r.currency}\n"
        f"Food: {r.food} {r.currency}\n"
        f"Transportation: {r.transportation} {r.currency}\n"
        f"Activities: {r.activities} {r.currency}\n"
        f"Total: {r.total} {r.currency}\n"
        f"Notes: {r.notes}"
    )
    return {
        "budget_info": budget_text
    }

# ==============================================================
# Planner Agent
# ==============================================================

def planner_agent(state: State) -> dict:
    user_request = state["user_request"]
    destination_info = state["destination_info"]
    food_info = state["food_info"]
    budget_info = state["budget_info"]

    prompt = [
        SystemMessage(
            content="""
            You are a travel planner.
            Combine the outputs of the destination, food and budget agents into one
            day-by-day travel plan that answers the user's request.
            Use ONLY the information provided by those agents - do NOT invent new
            attractions, restaurants or prices. If something is missing, say so.
            End with the budget summary.
            """
        ),
        HumanMessage(
            content=f"""
            User Request: {user_request}

            Destination Agent Output:
            {destination_info}

            Food Agent Output:
            {food_info}

            Budget Agent Output:
            {budget_info}
            """
        )
    ]

    response = llm.invoke(prompt)
    return {
        "final_plan": response.text
    }

# ==============================================================
# Graph
# ==============================================================

#                     ┌──→ Destination Agent ──┐
#                     │                         │
# START ──────────────┼──→ Food Agent ─────────┼──→ Planner Agent ──→ END
#                     │                         │
#                     └──→ Budget Agent ───────┘

builder = StateGraph(State)

builder.add_node("destination", destination_agent)
builder.add_node("food", food_agent)
builder.add_node("budget", budget_agent)
builder.add_node("planner", planner_agent)

builder.add_edge(START, "destination")
builder.add_edge(START, "food")
builder.add_edge(START, "budget")
builder.add_edge("destination", "planner")
builder.add_edge("food", "planner")
builder.add_edge("budget", "planner")
builder.add_edge("planner", END)

graph = builder.compile()

# ==============================================================
# Graph Execution
# ==============================================================

initial_state = {
    "user_request": "მინდა 4 დღით წავიდე პარიზში. მაინტერესებს მუზეუმები, კარგი ადგილობრივი საჭმელი და საშუალო ბიუჯეტი მაქვს.",
    "destination_info": "",
    "food_info": "",
    "budget_info": "",
    "final_plan": ""
}

result = graph.invoke(initial_state)
print(result["final_plan"])
