from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    plan: str
    used_credits: int
