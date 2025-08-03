from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Query
from fastapi.responses import RedirectResponse, JSONResponse
import os
import httpx
import uuid
from fastapi import FastAPI, HTTPException, Depends
from dotenv import load_dotenv
from routes import users, places
app = FastAPI()
load_dotenv()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
origins = [
    "http://localhost:19006",
   "https://rapidly-uncommon-kiwi.ngrok-free.app",
   
]
# Allow frontend (Expo) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # You can later restrict to ["http://localhost:19006"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router, prefix="/users")
app.include_router(places.router, prefix="/places")
