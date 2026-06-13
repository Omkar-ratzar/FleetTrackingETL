#Now we will be simulating a single truck going from lets say Pune to Udgir.
from geopy.distance import geodesic
import pandas as pd
from datetime import time,datetime,timedelta,date
import random

start_time= datetime.combine(date.today(),time(8, 30, 0))

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

def distance_bw(starting_point,ending_point):
    distance_km = geodesic(

        (starting_point["Latitude"], starting_point["Longitude"]),
        (ending_point["Latitude"], ending_point["Longitude"])
    ).km
    return round(distance_km,3)
# print("\n\n\n\n\n\n")

starting_point=df_points.iloc[0]
ending_point=df_points.iloc[-1]
# end_time=start_time+timedelta(hours=)

total=distance_bw(starting_point=starting_point,ending_point=ending_point)

print("Total Distance: ",total)
print("Fuel Needed: ",total/truck_mileage)
print("Price @ 99.6/L: ",99.69*(total/truck_mileage))
print("Time @ 40kmph: ", total/40)
print(f"Start time: {start_time} | End time: {start_time+timedelta(hours=total/40)}")


def speed_randomizer(speed):
    acceleration=[-11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    # if(speed>80):
    #     acceleration=range(-30,0)
    if(speed>60):
        acceleration=[-11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
    if(speed<15):
         acceleration=[-1,-2,-3,-4,0, 1, 2, 3, 4, 5, 6, 7, 8]
    if(speed<5):
         acceleration=[ 1, 2, 3, 4, 5]

    # plus_minus=0
    plus_minus=random.choice(acceleration)
    while(speed+plus_minus<0):
        plus_minus=random.choice(acceleration)
    return speed+plus_minus


#now I need to go from each point to point in geolocation csv files...

current_speed=speed_randomizer(0)
#start time alr initialized

point_csv_index=0
end_time=start_time
complete_distance=0

while( point_csv_index < (len(df_points) - 1)):

    starting_point=df_points.iloc[point_csv_index]
    ending_point=df_points.iloc[point_csv_index+1]
    # end_time=start_time+timedelta(hours=)
    this_section=distance_bw(starting_point=starting_point,ending_point=ending_point)
    if(current_speed>0):
        end_time+=timedelta(hours=this_section/current_speed)
    else:
        end_time+=timedelta(minutes=10)
        # print("REACHED 0!")
    complete_distance+=this_section

    current_speed=speed_randomizer(current_speed)
    # print(current_speed)
    point_csv_index+=1

actual_journey_time=end_time-start_time
avg_speed=complete_distance/(actual_journey_time.total_seconds()/3600)
print(complete_distance,start_time,end_time,actual_journey_time,round(avg_speed,2))

