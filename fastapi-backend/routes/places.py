from fastapi.responses import JSONResponse
from schemas.place import PlaceCreate,PlaceInDB
from fastapi import APIRouter
from mongodb import places_collection
from schemas.place import PlaceInput
from schemas.user import UserIdRequest
from bson import ObjectId
from ai import extract_place_info
from google_maps import get_google_maps_info 
router = APIRouter()
#user_id: str
from fastapi import Query


@router.post("/add_place", response_model=PlaceInDB)
async def create_place(place: PlaceInput):
    #get data from AI
    place_data = await extract_place_info(place.text)
    place_data["user_id"] = place.user_id
    # get google maps url
    place_name = place_data["name"]
    location_hint = place_data["address_hint"]
    if place_name != "Unknown":
        google_maps_info = await get_google_maps_info(place_name, location_hint)
        place_data["google_maps_url"] = google_maps_info["google_maps_url"] if "google_maps_url" in google_maps_info else None
        place_data["address_hint"] = google_maps_info["address"] if "address" in google_maps_info else place_data["address_hint"]
        place_data["name"] = google_maps_info["name"] if "name" in google_maps_info else place_data["name"]
        place_data["rating"] = google_maps_info["rating"] if "rating" in google_maps_info else None
    result = await places_collection.insert_one(place_data)
    return PlaceInDB(place_id=str(result.inserted_id), **place_data)

@router.get("/get_all_places_for_user", response_model=list)
async def get_places_for_user(user_id: str = Query(...)):
    places = await places_collection.find({"user_id": user_id}).to_list(length=100)
    for place in places:
        place["place_id"] = str(place["_id"])
        del place["_id"]
    return places

