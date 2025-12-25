from geopy.geocoders import Nominatim
import requests
from config import GEOAPIFY_API_KEY

geolocator = Nominatim(user_agent="therapy_finder")

def geocode_location(location: str):
    loc = geolocator.geocode(location)
    if not loc:
        return None
    return loc.latitude, loc.longitude


def find_nearby_therapists_by_location(location: str) -> str:
    coords = geocode_location(location)
    if not coords:
        return "Location not found"

    lat, lon = coords

    url = "https://api.geoapify.com/v2/places"
    params = {
        "categories": "healthcare.clinic_or_praxis.psychiatry,healthcare.clinic_or_praxis",
        "filter": f"circle:{lon},{lat},5000",
        "limit": 10,
        "apiKey": GEOAPIFY_API_KEY
    }

    response = requests.get(url, params=params, timeout=15)



    if response.status_code != 200:
        return "Geoapify API error"

    data = response.json()
    


    output = [f"Therapists near {location}:"]

    count = 0
    for feature in data.get("features", []):
        props = feature.get("properties", {})

        name = props.get("name", "Unknown")
        address = props.get("formatted", "Address not available")

        phone = (
            props.get("contact", {}).get("phone")
            or props.get("datasource", {}).get("raw", {}).get("phone")
            or "Phone not available"
        )

        output.append(f"- {name} | {address} | {phone}")

        count += 1
        if count == 5:
            break

    return "\n".join(output) if count > 0 else "No therapists found nearby"


# print(find_nearby_therapists_by_location("berlin"))