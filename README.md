# Places From Reels

Extract real‑world venues from Instagram Reels using AI and map them.  This full‑stack app lets you paste or share a Reel's caption/transcript, automatically extract place names using OpenAI, enrich them with Google Maps data (address, rating, link), and manage favourites in a mobile app.

## Features

- **Share Reel text**: Paste or share Instagram Reel captions and transcripts.
- **AI‑powered extraction**: Location names are identified via OpenAI’s language models.
- **Google Maps enrichment**: Match each candidate with the official place name, address, rating and a Google Maps link.
- **Save favourites**: Users can save favourite places per account and toggle between all places and favourites.
- **Mobile‑first**: A cross‑platform React Native app provides a friendly UI for login, adding Reel text, viewing place details and opening them in Google Maps.

## Tech Stack

### Backend (`/fastapi-backend`)

- **FastAPI** – asynchronous Python framework.
- **MongoDB** – stores users and places.
- **OpenAI API** – extracts structured place data from free‑form text; configured with `OPEN_AI_KEY`.
- **Google Maps API** – enriches place names with address, rating and map URL; uses `GOOGLE_MAPS_API_KEY`.

### Frontend (`/my-reel-map`)

- **React Native (Expo)** – cross‑platform mobile app.
- **Axios** – HTTP client to call the backend API.
- **Google Maps links** – open enriched places directly in Maps.

## Architecture Overview

This repo contains a Python FastAPI backend and a React Native Expo app.  The typical flow is:

1. **User logs in** or registers via `POST /users/create_user`.  
2. **User shares Reel text** through the mobile app.  The frontend calls `POST /places/add_place` with `{ "user_id": "...", "text": "<reel caption>" }`.  
3. **AI extraction**: the backend uses the OpenAI API to parse the caption into structured fields—name, city, address_hint, type and a brief summary.  
4. **Place enrichment**: the backend calls Google Maps Places API to match the name + location hint and retrieve the official name, formatted address, rating and a Maps URL.  
5. **Persistence**: the normalized place data is stored in MongoDB under the user’s document.  
6. **List and favourites**: the frontend fetches all places via `GET /places/get_all_places_for_user` and displays them; users can mark favourites via `POST /users/add_favorite_place` and retrieve them via `GET /users/get_favorite_places`.  
7. **Open Map**: tapping a place opens the Google Maps URL in the device’s browser.

#### Simplified flow diagram

```
React Native App (Expo)
      |
      | POST /places/add_place (user_id, text)
      v
FastAPI backend
      |
    [OpenAI] --extract--> structured place info
      |
    [Google Maps] --match--> address, rating, URL
      |
    MongoDB ←--- save
```

## Repository Layout

```
places-from-Reels/
├─ fastapi-backend/      # FastAPI service (AI extraction + Google Places + MongoDB)
│  ├─ main.py            # App init; sets CORS; mounts routers at /users and /places
│  ├─ ai.py              # Uses AsyncOpenAI to extract place data; reads OPEN_AI_KEY
│  ├─ google_maps.py     # Calls Google Places to enrich names; reads GOOGLE_MAPS_API_KEY
│  ├─ mongodb.py         # Connects to MongoDB via MONGO_URL and selects 'reel_map' DB
│  ├─ routes/            
│  │  ├─ users.py        # POST /users/create_user; POST /users/add_favorite_place; GET /users/get_favorite_places
│  │  └─ places.py       # POST /places/add_place; GET /places/get_all_places_for_user
│  └─ schemas/           # Pydantic models for validation (PlaceCreate, PlaceInDB, UserCreate, etc.)
├─ my-reel-map/          # React Native app (Expo)
│  ├─ app/               # expo-router screens
│  │  ├─ index.tsx                   # login screen; calls addUser
│  │  └─ user/
│  │     ├─ list_screen.tsx          # lists places; toggle favourites; open Google Maps
│  │     ├─ add_reel_screen.tsx      # paste Reel text; calls add_place
│  │     └─ place_details_screen.tsx # show place details; open link
│  ├─ api/api.ts         # Axios client for backend endpoints (set API_BASE_URL)
│  ├─ package.json       # NPM and Expo dependencies
│  └─ README.md          # Default Expo instructions (can be removed)
└─ README.md             # This file
```

## Getting Started

### Prerequisites

- **Python 3.11+**
- **Node.js 20+** and **npm** / **pnpm**
- **Expo CLI** (install globally via `npm install -g expo-cli`)
- **MongoDB** (local instance or Atlas cluster)
- **API keys** for OpenAI and Google Maps

### Backend Setup

1. Navigate into the backend folder and create a virtual environment:

   ```bash
   cd fastapi-backend
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install fastapi uvicorn motor pydantic httpx openai python-dotenv bson
   ```

3. Create a `.env` file with your secrets:

   ```
   OPEN_AI_KEY=sk-<your-openai-key>
   GOOGLE_MAPS_API_KEY=<your-google-maps-key>
   MONGO_URL=mongodb://localhost:27017
   GOOGLE_CLIENT_ID=<optional for OAuth>
   GOOGLE_CLIENT_SECRET=<optional>
   REDIRECT_URI=http://localhost:8000/auth/callback
   ```

   These environment variables are loaded in the code.

4. Start the server:

   ```bash
   uvicorn main:app --reload --port 8000
   ```

   The server exposes routes under `/users` and `/places`.

### Frontend Setup

1. Navigate into the React Native app:

   ```bash
   cd my-reel-map
   npm install
   ```

2. Update the API base URL:

   The file `api/api.ts` defines `API_BASE_URL` as an ngrok URL.  For local development change it to `http://localhost:8000`:

   ```ts
   const API_BASE_URL = "http://localhost:8000";
   ```

3. Start the app:

   ```bash
   npx expo start
   ```

   Use Expo Go or an emulator to run the mobile app.

## API Reference

### Users

- `POST /users/create_user` – Create or fetch a user by email.  
  **Body:** `{ "name": "Alice", "email": "alice@example.com" }`  
  **Response:** `{ "id": "<userId>", "name": "Alice", "email": "alice@example.com", "favorite_places": [] }`.

- `POST /users/add_favorite_place` – Add a place to a user’s favourites.  
  **Query parameters:** `place_id=<placeId>&user_id=<userId>`.  
  **Response:** Updated user record with the new favourite list.

- `GET /users/get_favorite_places` – Return an array of favourite place IDs for a user.

### Places

- `POST /places/add_place` – Extract and create a new place.  
  **Body:** `{ "user_id": "<userId>", "text": "<reel caption>" }`.  
  **Process:** uses OpenAI to extract the place and Google Maps to enrich the info.  
  **Response:** a `PlaceInDB` with fields like name, city, address_hint, rating and `google_maps_url`.

- `GET /places/get_all_places_for_user` – List all places for a user.  
  **Query parameter:** `user_id=<userId>`.

## Usage Example (cURL)

```bash
# 1. Create a user
curl -X POST http://localhost:8000/users/create_user \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com"}'

# 2. Add a place from a Reel caption
curl -X POST http://localhost:8000/places/add_place \
  -H "Content-Type: application/json" \
  -d '{"user_id":"<userId>","text":"I loved visiting Cafe Europa on Rothschild Blvd!"}'

# 3. List saved places
curl "http://localhost:8000/places/get_all_places_for_user?user_id=<userId>"

# 4. Add a favourite
curl -X POST "http://localhost:8000/users/add_favorite_place?place_id=<placeId>&user_id=<userId>"

# 5. List favourite place IDs
curl "http://localhost:8000/users/get_favorite_places?user_id=<userId>"
```

## Why These Technologies?

- **FastAPI** offers automatic OpenAPI docs, async performance and type hints, making it ideal for lightweight microservices and AI tasks.
- **MongoDB** provides a flexible document schema that fits semi‑structured place data and scales easily.
- **OpenAI API** handles natural language understanding such as extracting place names from free‑form text.
- **Google Maps API** supplies authoritative place details and deep links to the map, ensuring users can immediately navigate to their destination.
- **React Native (Expo)** enables a single codebase for iOS and Android with rapid iteration and easy access to device capabilities.
- **Axios** simplifies HTTP requests and interceptors in the frontend.

## Contributing

Contributions are welcome!  Please fork the repository, create a new branch for your feature or fix, and open a pull request.  Suggestions for additional features (e.g., social sharing, tags, offline support) are appreciated.

## License

Add your chosen license (e.g., MIT, Apache‑2.0) here.
