#MongoDB user model
from fastapi import FastAPI, Request, Depends
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import Optional
from typing import List, Optional
from pydantic import BaseModel

class User(BaseModel):
    id: str
    name: Optional[str] = None
    email: Optional[str] = None
    favorite_places: Optional[List[str]] = None


class Place(BaseModel):
    placeId: str
    UserId: str
    placeName: str
    city: Optional[str] = None
    address_hint: Optional[str] = None
    type: Optional[str] = None
    summarize: Optional[str] = None
    rating: Optional[float] = None
    google_maps_url: Optional[str] = None



