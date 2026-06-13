#Now we will be simulating a single truck going from lets say Pune to Udgir.
from geopy.distance import geodesic
import pandas as pd
df_points=pd.read_csv("E:\\Coding\\Fleet\\CSV_FILES\\pune_to_udgir_route.csv") #dataset of 467 points bw Pune and Udgir
df_trucks=pd.read_csv("E:\\Coding\\Fleet\\CSV_FILES\\truck_transformed.csv") #dataset of a 100 trucks


# print(df_trucks.iloc[0]["brand"])
#selecting the first truck for this simulattion
first_truck=df_trucks.iloc[0]

truck_name=first_truck["brand"]+" "+first_truck["model"]
truck_fuel_type=first_truck["fuel_type"]
truck_capacity=int(first_truck["fuel_tank"][:-3])
truck_mileage=int(first_truck["mileage"][:-5])
# print(truck_name,truck_capacity,truck_fuel_type,truck_mileage)

# print("\n\n\n\n\n\n")

starting_point=df_points.iloc[0]
ending_point=df_points.iloc[-1]

def distance_bw(starting_point,ending_point):
    distance_km = geodesic(

        (starting_point["Latitude"], starting_point["Longitude"]),
        (ending_point["Latitude"], ending_point["Longitude"])
    ).km
    return round(distance_km,3)

total=distance_bw(starting_point=starting_point,ending_point=ending_point)
print("Total Distance: ",total)
print("Fuel Needed: ",total/truck_mileage)
print("Price @ 99.6/L: ",99.69*(total/truck_mileage))
