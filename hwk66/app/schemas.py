from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    """What the client sends in POST /tasks."""

    title: str
    description: str = ""
    is_completed: bool = False


class TaskRead(TaskCreate):
    """What the API returns (includes the database-generated id)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
