import httpx
import os
from dotenv import load_dotenv
load_dotenv()  # ✅ Load from .env file


async def get_google_maps_info(name: str, location: str) -> dict:
    endpoint = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": os.getenv("GOOGLE_MAPS_API_KEY"),
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.googleMapsLinks.placeUri,places.rating"
    }
    payload = {"textQuery": f"{name}, {location}"}

    async with httpx.AsyncClient() as client:
        response = await client.post(endpoint, headers=headers, json=payload)
        data = response.json()

    try:
        place = data["places"][0]
        
        return {
            "name": place["displayName"]["text"],
            "address": place["formattedAddress"],
            "google_maps_url": place["googleMapsLinks"]["placeUri"],
            "rating": str(place["rating"]) 
            
        }
    except (KeyError, IndexError):
        return {"error": "Place not found"}
