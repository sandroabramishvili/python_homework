from uuid import uuid4

from schemas import TravelPlanRequest, TravelPlanResponse

from fastapi import FastAPI, HTTPException, Request
from database import lifespan

app = FastAPI(
    title="Multi-Agent Travel Planner",
    description="A service that plans travel using multiple AI agents",
    version="0.1.0",
    lifespan=lifespan
)

def make_config(thread_id: str):
    return {
        "configurable": {
            "thread_id": thread_id
        }
    }

def build_response(thread_id: str, snapshot):
    values = snapshot.values

    return TravelPlanResponse(
        thread_id=thread_id,
        user_request=values.get("user_request", ""),
        destination_info=values.get("destination_info"),
        food_info=values.get("food_info"),
        budget_info=values.get("budget_info"),
        final_plan=values.get("final_plan")
    )

@app.get("/")
def read_root():
    return {
        "service": "Multi-Agent Travel Planner",
        "version": "0.1.0",
        "status": "running"
    }

@app.post("/api/travel-plan", response_model=TravelPlanResponse)
def create_travel_plan(request: TravelPlanRequest, http_request: Request):

    graph = http_request.app.state.graph

    thread_id = str(uuid4())

    config = make_config(thread_id)

    initial_state = {
        "user_request": request.request,
        "destination_info": "",
        "food_info": "",
        "budget_info": "",
        "final_plan": ""
    }

    try:
        graph.invoke(
            initial_state,
            config=config
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Travel planner failed: {e}"
        )

    snapshot = graph.get_state(config)

    return build_response(thread_id, snapshot)


@app.get("/api/travel-plan/{thread_id}", response_model=TravelPlanResponse)
def get_travel_plan(thread_id: str, http_request: Request):

    graph = http_request.app.state.graph

    config = make_config(thread_id)

    try:
        snapshot = graph.get_state(config)
    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Travel plan not found"
        )

    if not snapshot.values:
        raise HTTPException(
            status_code=404,
            detail="Travel plan not found"
        )

    return build_response(thread_id, snapshot)
