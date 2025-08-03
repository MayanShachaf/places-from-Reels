from pydantic import BaseModel
from typing import Optional, List

# Used for user registration or login
class UserCreate(BaseModel):
    name: str
    email: str

# Used when fetching from the database
class UserInDB(UserCreate):
    id: str
    favorite_places: Optional[List[str]] = []
# Used for requests that require user identification
class UserIdRequest(BaseModel):
    user_id: str