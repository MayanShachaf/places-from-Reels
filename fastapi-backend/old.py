from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Query
from fastapi.responses import RedirectResponse, JSONResponse
from urllib.parse import urlencode
import os
import httpx
import uuid
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from google_drive import create_kml_file
from dotenv import load_dotenv
app = FastAPI()
load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

origins = [
    "http://localhost:19006",
    "https://6a1baf8d51d4.ngrok-free.app",
]
# Allow frontend (Expo) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # You can later restrict to ["http://localhost:19006"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users_name_and_id = {}
files = {}
@app.get("/get_id")
def get_id():
    # Generate a unique ID for the user session
    user_id = str(uuid.uuid4())
    # Store the user ID in the session dictionary
    users_name_and_id[user_id] = None
    # Return the user ID
    return {"id": user_id}

@app.get("/auth/login/{user_id}}")
def login(user_id: str):
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    
    }
    params["state"] = user_id  # <-- Pass the user ID as state
    url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    return RedirectResponse(url)

@app.get("/auth/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    id = request.query_params.get("state")  # <-- Get state from query params
    if not code:
        return JSONResponse({"error": "Missing code"})
    if not id:
        return JSONResponse({"error": "Missing id"})
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": REDIRECT_URI
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
    if token_resp.status_code != 200:
        return JSONResponse({"error": "Failed to fetch token"}, status_code=400)
    token_data = token_resp.json()
    access_token = token_data.get("access_token")

    async with httpx.AsyncClient() as client:
        user_info_resp = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
    user_info = user_info_resp.json()
    user_name = user_info.get("name")
    print("access_token:", access_token)
    # put the user name for the id
    users_name_and_id[id] = user_name
    

    # Redirect back to Expo Auth with session_id
    #app_redirect_url = "https://auth.expo.io/@mayan.shac/my-reel-map"
    #params = urlencode({"session_id": session_id})
    #return RedirectResponse(f"{app_redirect_url}?{params}")
    return HTMLResponse(f"<h1>Hello, {user_name}! Please return to the app to countinue the set up :) .</h1>")
@app.get("/auth/user")
def get_user(session_id: str = Query(...)):
    user_name = user_sessions.get(session_id)
    if user_name:
        return {"name": user_name}
    return JSONResponse({"error": "User not found"}, status_code=404)

