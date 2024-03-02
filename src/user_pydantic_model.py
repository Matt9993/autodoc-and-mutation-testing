from pydantic import BaseModel

class DummyUser(BaseModel):
    user_id: int
    name: str = "Jane Doe"
