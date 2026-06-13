import csv
import requests
import folium
from folium import Map
from geopy import Nominatim
from pydantic import BaseModel

geolocator = Nominatim(user_agent="my_coordinate_finder")

class Point(BaseModel):
    latitude: float
    longitude: float
def get_osrm_route_points(start: Point, end: Point) -> list[Point]:

    coords = (
        f"{start.longitude},{start.latitude};"
        f"{end.longitude},{end.latitude}"
    )

    url = (
        f"https://router.project-osrm.org/"
        f"route/v1/driving/{coords}"
    )

    params = {
        "overview": "full",
        "geometries": "geojson"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    raw_coords = data["routes"][0]["geometry"]["coordinates"]

    return [
        Point(latitude=lat, longitude=lon)
        for lon, lat in raw_coords
    ]

def get_folium_map(center_point: Point, points: list[Point], zoom_level: int = 8) -> Map:
    folium_map = folium.Map(
        location=[center_point.latitude, center_point.longitude], zoom_start=zoom_level, tiles="CartoDB positron")

    for point in points:
        folium.Marker(location=[point.latitude, point.longitude],
                      popup='Point').add_to(folium_map)

    return folium_map

def save_points_to_csv(points: list[Point], filename="CSV_FILES//pune_to_udgir_route.csv"):
    """Saves the sampled points list directly to a clean CSV dataset."""
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Index", "Latitude", "Longitude"])
        for idx, pt in enumerate(points):
            writer.writerow([idx, pt.latitude, pt.longitude])
    print(f"\n[SUCCESS] Saved {len(points)} points straight to '{filename}'")


# --- Execution Flow ---
location1 = "Wakad, Pune"
location2 = "Udgir"

print("Geocoding locations...")
loc1 = geolocator.geocode(location1)
loc2 = geolocator.geocode(location2)

Wakad_point = Point(
    latitude=loc1.latitude,
    longitude=loc1.longitude
)

Udgir_point = Point(
    latitude=loc2.latitude,
    longitude=loc2.longitude
)

print("Fetching route from OSRM...")
all_route_points = get_osrm_route_points(Wakad_point, Udgir_point)

# Samples every 10th coordinate along the path
sampled_points = all_route_points[::10]

# Ensure destination stays in the dataset
if sampled_points[-1] != all_route_points[-1]:
    sampled_points.append(all_route_points[-1])

# Save output data
save_points_to_csv(sampled_points)

print("Generating map file...")
folium_map = get_folium_map(Wakad_point, sampled_points)
folium_map.save("my_map.html")
print("[SUCCESS] 'my_map.html' ready.")
