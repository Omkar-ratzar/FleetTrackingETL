import csv
import requests
import folium
from folium import Map
from geopy import Nominatim
from pydantic import BaseModel
import random
# from collections import defaultdict
import time
geolocator = Nominatim(user_agent="my_coordinate_finder")

class Point(BaseModel):
    latitude: float
    longitude: float

#refactoring for multiple locations across India
Cities = [
    # Top 30 cities by population
    "Delhi",
    "Mumbai",
    "Kolkata",
    "Bengaluru",
    "Chennai",
    "Hyderabad",
    "Ahmedabad",
    "Pune",
    "Surat",
    "Jaipur",
    "Lucknow",
    "Kanpur",
    "Nagpur",
    "Indore",
    "Patna",
    "Bhopal",
    "Visakhapatnam",
    "Ludhiana",
    "Agra",
    "Nashik",
    "Vadodara",
    "Faridabad",
    "Meerut",
    "Rajkot",
    "Varanasi",
    "Srinagar",
    "Aurangabad",
    "Dhanbad",
    "Amritsar",
    "Prayagraj",
    # State capitals not already included
    "Itanagar",
    "Dispur",
    "Chandigarh",
    "Raipur",
    "Panaji",
    "Gandhinagar",
    "Shimla",
    "Ranchi",
    "Thiruvananthapuram",
    "Bhopal",
    "Mumbai",
    "Imphal",
    "Shillong",
    "Aizawl",
    "Kohima",
    "Bhubaneswar",
    "Gangtok",
    "Chennai",
    "Hyderabad",
    "Agartala",
    "Dehradun",
    # Union Territory capitals
    # "Port Blair",
    "Chandigarh",
    "Daman",
    # "Kavaratti",
    "Leh",
    "Jammu",
    "Puducherry",
    "Delhi",
    "Srinagar"
]

def get_osrm_route_points(start: Point, end: Point) -> list[Point]:
    try:
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

        response = requests.get(url, params=params,timeout=30)
        response.raise_for_status()

        data = response.json()

        raw_coords = data["routes"][0]["geometry"]["coordinates"]

        return [
            Point(latitude=lat, longitude=lon)
            for lon, lat in raw_coords
        ]
    except Exception as e:
        print(e)


def get_folium_map(center_point: Point, points: list[Point], zoom_level: int = 8) -> Map:
    folium_map = folium.Map(
        location=[center_point.latitude, center_point.longitude], zoom_start=zoom_level, tiles="CartoDB positron")

    for point in points:
        folium.Marker(location=[point.latitude, point.longitude],
                    popup='Point').add_to(folium_map)

    return folium_map


def save_points_to_csv(From,To,points: list[Point]):
    filename=f"CSV_FILES//Routes//{From}_to_{To}_route.csv"

    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Index", "Latitude", "Longitude"])
        for idx, pt in enumerate(points):
            writer.writerow([idx, pt.latitude, pt.longitude])
    print(f"\n[SUCCESS] Saved {len(points)} points straight to '{filename}'")



#there arent any duplicates but just for the sake of code :)
Cities=list(set(Cities))

#HASHMAP to store city's geocodes so no repeated geocoding
geocoder={}
for route_index in range(100):

    location1 = random.choice(Cities)
    # excl=Cities.remove(location1) Noobie. Bruh.
    excl=Cities.copy()
    excl.remove(location1)
    location2 = random.choice(excl) #ensuring that it will be a different city.

    print("Geocoding locations...")
    if(location1 in geocoder):
        First_City_Point = Point(
        latitude=geocoder[location1][0],
        longitude=geocoder[location1][1]
        )
    else:
        time.sleep(1)#Rate limiting the reqz

        loc1 = geolocator.geocode(location1)
        if loc1 is None:
            print(f"Failed to geocode {location1}")
            continue
        First_City_Point = Point(
            latitude=loc1.latitude,
            longitude=loc1.longitude
        )
        geocoder[location1]=First_City_Point.latitude,First_City_Point.longitude
    if(location2 in geocoder):
        Second_City_Point = Point(
        latitude=geocoder[location2][0],
        longitude=geocoder[location2][1]
    )
    else:
        time.sleep(1)#Rate limiting the reqz

        loc2 = geolocator.geocode(location2)
        if loc2 is None:
            print(f"Failed to geocode {location2}")
            continue
        Second_City_Point = Point(
            latitude=loc2.latitude,
            longitude=loc2.longitude
        )
        geocoder[location2]=Second_City_Point.latitude,Second_City_Point.longitude

    print("Fetching route from OSRM...")
    all_route_points = get_osrm_route_points(First_City_Point, Second_City_Point)

    if not all_route_points:
        print(f"Failed route: {location1} -> {location2}")
        continue

    # Samples every 9th coordinate along the path
    sampled_points = all_route_points[::9]

    # Ensure destination stays in the dataset
    if sampled_points[-1] != all_route_points[-1]:
        sampled_points.append(all_route_points[-1])

    # Save output data
    save_points_to_csv(location1,location2,sampled_points)

    # print("Generating map file...")
    # folium_map = get_folium_map(First_City_Point, sampled_points)
    # folium_map.save("my_map.html")
    # print("[SUCCESS] 'my_map.html' ready.")
