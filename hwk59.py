from dotenv import load_dotenv
load_dotenv()

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI

MODEL = "gemini-3.5-flash-lite"
MAX_ATTEMPTS = 3

llm = ChatGoogleGenerativeAI(
        model=MODEL
    )

class State(TypedDict):
    ingredients: str
    recipe: str
    feedback: str
    approved: bool
    attempts: int

class RecipeCheck(TypedDict):
    """Feedback on a recipe and whether it is approved."""
    feedback: str
    approved: bool

checker_llm = llm.with_structured_output(RecipeCheck)

def generate_recipe(state: State) -> State:

    prompt = f"""
    You are a recipe generation model.
    Create a simple recipe using the following ingredients:
    {state['ingredients']}
    Return only the recipe.
    """

    response = llm.invoke(prompt)

    return {
        "recipe": response.text
    }

def check_recipe(state: State) -> State:

    prompt = f"""
    You are a recipe checking model.
    Check the following recipe for the given ingredients:
    Ingredients: {state['ingredients']}
    Recipe: {state['recipe']}
    Are the ingredients used correctly?
    Is the recipe clear and understandable?
    Does it include all necessary preparation steps?
    Are the ingredient quantities logical?
    Provide feedback and indicate if the recipe is approved.
    """

    result = checker_llm.invoke(prompt)
    attempts = state["attempts"] + 1
    print(f"[check_recipe] attempt {attempts}: approved={result['approved']} | {result['feedback']}")

    return {**result, "attempts": attempts}

def route_after_check_recipe(state: State) -> str:
    if state["approved"]:
        return END
    if state["attempts"] >= MAX_ATTEMPTS:
        print(f"[route] Recipe not approved after {MAX_ATTEMPTS} attempts, stopping.")
        return END
    return "improve"

def improve_recipe(state: State) -> State:

    prompt = f"""
    You are a recipe improvement model.
    Improve the following recipe based on the feedback:
    Ingredients: {state['ingredients']}
    Recipe: {state['recipe']}
    Feedback: {state['feedback']}
    Return only the improved recipe.
    """

    response = llm.invoke(prompt)

    return {
        "recipe": response.text
    }

builder = StateGraph(State)

builder.add_node("generate_recipe", generate_recipe)
builder.add_node("check_recipe", check_recipe)
builder.add_node("improve", improve_recipe)

builder.add_edge(START, "generate_recipe")
builder.add_edge("generate_recipe", "check_recipe")
builder.add_conditional_edges("check_recipe", route_after_check_recipe, ["improve", END])
builder.add_edge("improve", "check_recipe")

graph = builder.compile()

result = graph.invoke({
    "ingredients": "chicken, rice, onion, tomato",
    "recipe": "",
    "feedback": "",
    "approved": False,
    "attempts": 0
})

print("\n========== RECIPE ==========")
print(result["recipe"])
print("\n========== FEEDBACK ==========")
print(result["feedback"])
print(f"\nApproved: {result['approved']} | Attempts: {result['attempts']}")
