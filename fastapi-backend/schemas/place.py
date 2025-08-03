from pydantic import BaseModel
from typing import Optional

# Place data extracted from AI and saved to DB
class PlaceCreate(BaseModel):
    user_id: str
    name: str
    city: Optional[str] = None
    address_hint: Optional[str] = None
    type: Optional[str] = None
    summarize: Optional[str] = None
    

class PlaceInput(BaseModel):
    user_id: str
    text: str
# Full place model with ID (from DB)
class PlaceInDB(PlaceCreate):
    place_id: str
    rating:  Optional[str] = None
    google_maps_url: Optional[str] = None
