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
print(truck_name,truck_capacity,truck_fuel_type,truck_mileage)

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

#wrong cz this will give me the displacement, will NOT use these values
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
current_fuel_percent=32 #keeping it 32% cz ofc no truck is always 100% filled and I can stimulate stops and I'd completely randomize this while refactoring for all trucks
current_fuel=current_fuel_percent/100*truck_capacity



point_csv_index=0
end_time=start_time
complete_distance=0

logger_list=[]

while( point_csv_index < (len(df_points) - 1)):
    state="Running"
    starting_point=df_points.iloc[point_csv_index]
    ending_point=df_points.iloc[point_csv_index+1]
    # end_time=start_time+timedelta(hours=)
    this_section=distance_bw(starting_point=starting_point,ending_point=ending_point)
    #fuel shit
    fuel_burnt=this_section/truck_mileage
    current_fuel-=fuel_burnt
    current_fuel_percent=current_fuel/truck_capacity*100
    if(current_fuel_percent<5):
        #add a stop of 10 mins and reset
        state="Fuel Stop"
        end_time+=timedelta(minutes=10)
        current_fuel=truck_capacity
        current_fuel_percent=100
    if(current_speed>0):
        end_time+=timedelta(hours=this_section/current_speed)
    else:
        #reached 0.
        #5 to 40 mins in traffic now
        state="Traffic"
        traffic_stop=random.choice(range(5,40))
        end_time+=timedelta(minutes=traffic_stop)

    complete_distance+=this_section

    # print(f"Current speed: {current_speed}, Length of this section: {this_section}, Current Fuel Capacity: {current_fuel_percent}")

    #to be stored in the csv file in each row: point_csv_index as idx, ending_point as curr_point, this_section as section_len, current_fuel_percent, current_speed,ending_time as Duration, state (default: Running, Traffic if traffic, fuelstop if fuelstop)
    log_row = {
        "idx": point_csv_index,
        "curr_lat": ending_point["Latitude"],
        "curr_lon": ending_point["Longitude"],
        "section_len": round(this_section, 3),
        "current_fuel_percent": round(current_fuel_percent, 2),
        "current_speed": current_speed,
        "duration": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "state": state
    }
    logger_list.append(log_row)
    current_speed=speed_randomizer(current_speed)
    # print(current_speed)
    point_csv_index+=1


actual_journey_time=end_time-start_time
avg_speed=complete_distance/(actual_journey_time.total_seconds()/3600)
print(complete_distance,start_time,end_time,actual_journey_time,round(avg_speed,2))
#print(logger_list)
df_journey=pd.DataFrame(logger_list)
output_path = "E:\\Coding\\Fleet\\CSV_FILES\\Journeys\\First_Journey_Ever.csv"
df_journey.to_csv(output_path,index=False)

