import requests
import os
import time
from dotenv import load_dotenv
import pandas as pd

# Load API Key
load_dotenv()
API_KEY = os.getenv("Google_Places_api")

def geocode(place):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": place,
        "key": API_KEY
    }
    res = requests.get(url, params=params).json()

    if not res.get("results"):
        return None

    loc = res["results"][0]["geometry"]["location"]
    return loc["lat"], loc["lng"]


def find_saloons(lat, lng, radius=3000):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "keyword": "parlour",
        "type": "men parlour",
        "key": API_KEY
    }
    res = requests.get(url, params=params).json()
    return res.get("results", [])


def get_contact_details(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": (
            "formatted_phone_number,"
            "international_phone_number,"
            "website,"
            "opening_hours.weekday_text,"
            "url"
        ),
        "key": API_KEY
    }

    res = requests.get(url, params=params).json()
    result = res.get("result", {})

    opening_hours = result.get("opening_hours", {}).get("weekday_text")

    return {
        "international_phone": result.get("international_phone_number"),
        "website": result.get("website"),
        "opening_hours": "; ".join(opening_hours) if opening_hours else None,
        "map_link": result.get("url")
    }


def format_results(results):
    saloons = []
    for r in results:
        saloons.append({
            "place_id": r.get("place_id"),
            "name": r.get("name"),
            "address": r.get("vicinity"),
            "rating": r.get("rating"),
            "total_reviews": r.get("user_ratings_total"),
            "open_now": r.get("opening_hours", {}).get("open_now")
        })
    return saloons


place = "Surathkal Mangalore"

coords = geocode(place)

if not coords:
    print("Location not found")
    exit()

lat, lng = coords
raw_results = find_saloons(lat, lng)
saloons = format_results(raw_results)

# Excel Columns
cols = [
    "name",
    "address",
    "rating",
    "open_now",
    "opening_hours",
    "international_phone",
    "website",
    "map_link"
]

data = {key: [] for key in cols}

for s in saloons[:35]:  # limit to avoid quota issues
    contact = get_contact_details(s["place_id"])
    s.update(contact)

    for key in cols:
        data[key].append(s.get(key))

    time.sleep(0.25) 

df = pd.DataFrame(data)

# Save to Excel
current_dir = os.getcwd()
file_name = "Backend_parlour_men_data.xlsx"
path = os.path.join(current_dir, file_name)

df.to_excel(path, index=False)

print("Completed Successfully...")
print(f" File saved at: {path}")
