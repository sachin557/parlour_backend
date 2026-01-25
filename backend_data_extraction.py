import requests
import os
import time
from dotenv import load_dotenv
import pandas as pd

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
        "keyword": "salon",
        "type": "beauty_salon",
        "key": API_KEY
    }

    res = requests.get(url, params=params).json()
    return res.get("results", [])


def get_contact_details(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "formatted_phone_number,international_phone_number,website",
        "key": API_KEY
    }

    res = requests.get(url, params=params).json()
    result = res.get("result", {})

    return {
        "phone": result.get("formatted_phone_number"),
        "international_phone": result.get("international_phone_number"),
        "website": result.get("website")
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



place = "Surathkal mangalore"

coords = geocode(place)
if not coords:
    print("Location not found")
else:
    lat, lng = coords
    raw = find_saloons(lat, lng)
    saloons = format_results(raw)

cols=["name","address","rating","open_now","international_phone","website"]
df=pd.DataFrame(columns=cols)
data={key:[] for key in cols}
for s in saloons[:25]:
    contact = get_contact_details(s["place_id"])
    s.update(contact)
    time.sleep(0.2)
    #print(s)
    for key,values in s.items():
        if key in cols:
            data[key].append(values)
df=pd.DataFrame(data)
current_dir=os.getcwd()
file="Backend_saloons_data.xlsx"
path=os.path.join(current_dir,file)
df.to_excel(path,index=False)
