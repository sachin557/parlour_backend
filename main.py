from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from aichat import chatbot

app = FastAPI(title="Salon Search API")

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- REQUEST MODEL ----------------
class Location(BaseModel):
    location_name: str

# ---------------- ROUTE ----------------
@app.post("/search-saloons")
async def search_saloons(data: Location):
    location = data.location_name.strip()

    if not location:
        raise HTTPException(status_code=400, detail="Location cannot be empty")

    # run Groq in threadpool
    result = await run_in_threadpool(chatbot, location)

    return result

# ---------------- HEALTH (UPTIMEROBOT SAFE) -----------------
@app.api_route("/health", methods=["GET", "HEAD", "POST"])
async def health(response: Response):
    response.headers["Cache-Control"] = "no-store"
    return {
        "status": "ok",
        "service": "salon-search-api"
    }
