#Now we will be simulating a single truck going from lets say Pune to Udgir.
from geopy.distance import geodesic
import pandas as pd
from datetime import time,datetime,timedelta,date
import random
from pathlib import Path



Routes = [f.name for f in Path('E:\\Coding\\Fleet\\CSV_FILES\\Routes').iterdir() if f.is_file()]
# print(Routes)

Total_Journeys=400

def speed_randomizer(speed):
    acceleration=[-11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    # if(speed>80):
    #     acceleration=range(-30,0)
    if(speed<5):
        acceleration=[ 1, 2, 3, 4, 5]
    elif(speed>60):
        acceleration=[-11, -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
    elif(speed<15):
        acceleration=[-1,-2,-3,-4,0, 1, 2, 3, 4, 5, 6, 7, 8]
    # plus_minus=0
    plus_minus=random.choice(acceleration)
    while(speed+plus_minus<0):
        plus_minus=random.choice(acceleration)
    return speed+plus_minus

def distance_bw(starting_point,ending_point):
    distance_km = geodesic(

        (starting_point["Latitude"], starting_point["Longitude"]),
        (ending_point["Latitude"], ending_point["Longitude"])
    ).km
    return round(distance_km,3)

df_trucks=pd.read_csv("E:\\Coding\\Fleet\\CSV_FILES\\truck_cleaned.csv") #dataset of a 435 trucks
for iterator in range(Total_Journeys):

    start_time = datetime.combine(date.today(),time(random.randint(5, 10),random.randint(0, 59)))
    route_choice=random.choice(Routes)
    df_points=pd.read_csv(f"E:\\Coding\\Fleet\\CSV_FILES\\Routes\\{route_choice}") #dataset of multiple points bw cities


    # print(df_trucks.iloc[0]["brand"])
    #selecting the first truck for this simulattion

    # Current_Truck=df_trucks.iloc[random.randint(0,len(df_trucks)-1)]
    Current_Truck=df_trucks.sample(1,replace=True).iloc[0]

    truck_name=Current_Truck["brand"]+" "+Current_Truck["model"]
    truck_fuel_type=Current_Truck["fuel_type"]
    truck_capacity=float(Current_Truck["fuel_tank_liters"])
    truck_mileage=float(Current_Truck["mileage_kmpl"])
    print(truck_name,truck_capacity,truck_fuel_type,truck_mileage)


    # print("\n\n\n\n\n\n")

    starting_point=df_points.iloc[0]
    ending_point=df_points.iloc[-1]
    # # end_time=start_time+timedelta(hours=)

    # #wrong cz this will give me the displacement, will NOT use these values
    # total=distance_bw(starting_point=starting_point,ending_point=ending_point)
    # print("Total Distance: ",total)
    # print("Fuel Needed: ",total/truck_mileage)
    # print("Price @ 99.6/L: ",99.69*(total/truck_mileage))
    # print("Time @ 40kmph: ", total/40)
    # print(f"Start time: {start_time} | End time: {start_time+timedelta(hours=total/40)}")




    #now I need to go from each point to point in geolocation csv files...

    current_speed=speed_randomizer(0)
    #start time alr initialized
    current_fuel_percent=random.randint(1,100) #keeping it 32% cz ofc no truck is always 100% filled and I can stimulate stops and I'd completely randomize this while refactoring for all trucks
    current_fuel=current_fuel_percent/100*truck_capacity



    point_csv_index=0
    end_time=start_time
    complete_distance=0

    logger_list=[]
    route_choice=route_choice[:-4] #removing the file extension to be used properly in the rest of the code

    #aading some inconsistencies throughtout the journey to make it more riyal. If any of these go true, these will occur in the journey.
    journey_len=len(df_points)
    tyre_puncture=False
    accident=False
    GPS_lost=False
    detour=False
    GPS_drift=False
    if(random.random()<0.005):
        tyre_puncture=True
        puncture_index=random.randint(max(5,journey_len//5),journey_len-5)
    if(random.random()<0.001):
        accident=True
        accident_index=random.randint(max(5,journey_len//5),journey_len-5)
    if(random.random()<0.05):
        GPS_lost=True
        GPS_lost_start=random.randint(2,journey_len-10)
        GPS_lost_length=random.randint(3,10)
    if(random.random()<0.01):
        detour=True
        detour_start=random.randint(5,journey_len-10)
        detour_length=random.randint(3,8)
    if(random.random()<0.03):
        GPS_drift=True
        GPS_drift_index=random.randint(2,journey_len-2)



    while( point_csv_index < (len(df_points) - 1)):
        # state="Running"
        starting_point=df_points.iloc[point_csv_index]
        ending_point=df_points.iloc[point_csv_index+1]
        # end_time=start_time+timedelta(hours=)
        this_section=distance_bw(starting_point=starting_point,ending_point=ending_point)
        #detour shi
        if(detour and detour_start<=point_csv_index<detour_start+detour_length):
            this_section*=random.uniform(1.5,2.5)

        #GPS loss shi
        if(GPS_lost and GPS_lost_start<=point_csv_index<GPS_lost_start+GPS_lost_length):
            if(current_speed>0):
                end_time+=timedelta(hours=this_section/current_speed)
            point_csv_index+=1
            continue


        #fuel shit
        fuel_burnt=this_section/truck_mileage
        current_fuel-=fuel_burnt
        current_fuel_percent=current_fuel/truck_capacity*100
        if(current_fuel_percent<5):
            #add a stop of 10 mins and reset
            # state="Fuel Stop"
            end_time+=timedelta(minutes=10)
            current_fuel=truck_capacity
            current_fuel_percent=100
        if(current_speed>0):
            end_time+=timedelta(hours=this_section/current_speed)
        else:
            #reached 0.
            #5 to 40 mins in traffic now
            # state="Traffic"
            # traffic_stop=random.choice(range(5,40))
            r=random.random()
            if(r<0.92):
                traffic_stop=random.randint(5,20)
            elif(r<0.99):
                traffic_stop=random.randint(30,60)
            elif(r<0.9999):
                traffic_stop=random.randint(70,240)
            else:
                traffic_stop=random.randint(300,1000)
            end_time+=timedelta(minutes=traffic_stop)

        complete_distance+=this_section
        if(tyre_puncture and point_csv_index==puncture_index):
            # state="Tyre Puncture"
            current_speed=0
            end_time+=timedelta(minutes=random.randint(20,90))
        if(accident and point_csv_index==accident_index):
            # state="Accident"
            current_speed=0

        #GPS drift.
        curr_lat=ending_point["Latitude"]
        curr_lon=ending_point["Longitude"]
        if(GPS_drift and point_csv_index==GPS_drift_index):
            curr_lat+=random.uniform(-0.0008,0.0008)
            curr_lon+=random.uniform(-0.0008,0.0008)

        # print(f"Current speed: {current_speed}, Length of this section: {this_section}, Current Fuel Capacity: {current_fuel_percent}")

        #to be stored in the csv file in each row: point_csv_index as idx, ending_point as curr_point, this_section as section_len, current_fuel_percent, current_speed,ending_time as Duration, state (default: Running, Traffic if traffic, fuelstop if fuelstop)
        log_row = {
            "journey_id":iterator,
            "truck_name": truck_name,
            "fuel_type":truck_fuel_type,
            "route_name":route_choice,
            "idx": point_csv_index,
            "curr_lat":curr_lat,
            "curr_lon": curr_lon,
            "section_len": round(this_section, 3),
            "current_fuel_percent": round(current_fuel_percent, 2),
            "current_speed": current_speed,
            "duration": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            # "state": state
        }
        logger_list.append(log_row)


        #accident, truck will stay on the same point forever
        # Journey ends here because of accident.
        # GPS tracker is still powered and keeps transmitting.
        #####
        if(accident and point_csv_index==accident_index):

            accident_hours = random.randint(3, 8)
            packet_interval = random.randint(3, 8)

            for _ in range((accident_hours*60)//packet_interval):
                end_time+=timedelta(minutes=packet_interval)
                logger_list.append({
                    "journey_id":iterator,
                    "truck_name":truck_name,
                    "fuel_type":truck_fuel_type,
                    "route_name":route_choice,
                    "idx":point_csv_index,
                    "curr_lat":curr_lat,
                    "curr_lon": curr_lon,
                    "section_len":0,
                    "current_fuel_percent":round(current_fuel_percent,2),
                    "current_speed":0,
                    "duration":end_time.strftime("%Y-%m-%d %H:%M:%S"),
                    # "state":"Accident"
                })
            break

        #####


        current_speed=speed_randomizer(current_speed)
        # print(current_speed)
        point_csv_index+=1


    actual_journey_time=end_time-start_time
    avg_speed=complete_distance/(actual_journey_time.total_seconds()/3600)
    print(complete_distance,start_time,end_time,actual_journey_time,round(avg_speed,2))
    #print(logger_list)
    df_journey=pd.DataFrame(logger_list)
    df_journey.head()
    len(df_journey)
    # output_path = f"E:\\Coding\\Fleet\\CSV_FILES\\Journeys\\{datetime.today()}\\{route_choice}.csv"
    today_folder = datetime.today().strftime("%Y-%m-%d")
    output_dir = f"E:\\Coding\\Fleet\\CSV_FILES\\Journeys\\{today_folder}"
    Path(output_dir).mkdir(parents=True, exist_ok=True) #ensuring the folder of that date exists
    output_path = output_dir+f"\\journey_{iterator}_{route_choice}.csv"
    df_journey.to_csv(output_path,index=False)

