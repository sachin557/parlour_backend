from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from typing import List, Dict, Optional
from Parlour_details_list import get_parlour_list   
from aichat import chatbot                        


# Naming the api
app = FastAPI(title="Salon Platform API")

# cors for taking any url *
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# setting the datatype for variable

class SalonRequest(BaseModel):
    gender: str       # men / women
    category: str  
    sort: str   # hair / spa / makeup


class AiSearchRequest(BaseModel):
    location_name: str


# saloon details search
@app.post("/search-saloons")
async def search_saloons(data: SalonRequest):
    gender = data.gender.strip().lower()
    category = data.category.strip().lower()
    sort_by_rating=data.sort.strip().lower()
    if gender not in {"men", "women"}:
        raise HTTPException(status_code=400, detail="Invalid gender")

    if category not in {"hair", "spa", "makeup"}:
        raise HTTPException(status_code=400, detail="Invalid category")

    try:
        results = await run_in_threadpool(
            get_parlour_list,
            gender,
            category,
            sort_by_rating
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for {gender} - {category}",
        )
    except Exception as e:
        print(" SALON EXCEL ERROR:", e)
        raise HTTPException(
            status_code=503,
            detail="Salon data service unavailable",
        )

    return {
        "gender": gender,
        "category": category,
        "count": len(results),
        "results": results,
    }


# ai chat search
@app.post("/ai-search")
async def ai_search(data: AiSearchRequest):
    location = data.location_name.strip()

    if not location:
        raise HTTPException(status_code=400, detail="Location cannot be empty")

    try:
        # Groq AI call
        result = await run_in_threadpool(
            chatbot,
            location,
        )
    except Exception as e:
        print(" AI SEARCH ERROR:", e)
        raise HTTPException(
            status_code=503,
            detail="AI search service unavailable",
        )

    return result


# Render ping to keep the backend alive 
@app.api_route("/health", methods=["GET", "HEAD"])
def health(response: Response):
    response.headers["Cache-Control"] = "no-store"
    return {
        "status": "ok",
        "service": "salon-platform-api"
    }
