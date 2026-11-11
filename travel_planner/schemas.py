from pydantic import BaseModel, Field

class BudgetResult(BaseModel):
    currency: str = Field(..., description="Currency code, e.g. EUR")
    accommodation: float = Field(..., description="Total accommodation cost for the whole trip")
    food: float = Field(..., description="Total food cost for the whole trip")
    transportation: float = Field(..., description="Total local and arrival transport cost")
    activities: float = Field(..., description="Total cost of tickets and activities")
    total: float = Field(..., description="Sum of all categories")
    notes: str = Field(..., description="Short assumptions behind the estimate")
    
# ==============================================================
# API Schemas
# ==============================================================

class TravelPlanRequest(BaseModel):
    request: str = Field(
        ...,
        min_length=10,
        description="The user's travel request: destination, trip length, interests, budget level",
        examples=["I want to spend 4 days in Paris. I like museums, good local food and have a medium budget."]
    )

class TravelPlanResponse(BaseModel):
    thread_id: str
    user_request: str
    destination_info: str | None = None
    food_info: str | None = None
    budget_info: str | None = None
    final_plan: str | None = None