from mongodb import users_collection
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from schemas.user import UserCreate, UserInDB
from bson import ObjectId

router = APIRouter()

@router.post("/create_user", response_model=UserInDB)
async def create_user(user: UserCreate):
    existing = await users_collection.find_one({"email": user.email})
    if existing:
        if existing:
            return UserInDB(
            id=str(existing["_id"]),
            name=existing["name"],
            email=existing["email"],
            favorite_places=existing.get("favorite_places", [])
            )
    result = await users_collection.insert_one(user.dict())
    return UserInDB(
        id=str(result.inserted_id),
        name=user.name,
        email=user.email,
        favorite_places=[]
    )
@router.post("/add_favorite_place", response_model=UserInDB)
async def add_favorite_place(place_id: str, user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if place_id not in user["favorite_places"]:
        user["favorite_places"].append(place_id)
        await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"favorite_places": user["favorite_places"]}})
        
    return UserInDB(
        id=str(user["_id"]),
        name=user.get("name"),
        email=user.get("email"),
        favorite_places=user["favorite_places"]
    )
    
@router.get("/get_favorite_places/", response_model=UserInDB)
async def get_user(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserInDB(
        id=str(user["_id"]),
        name=user.get("name"),
        email=user.get("email"),
        favorite_places=user.get("favorite_places", [])
    )


