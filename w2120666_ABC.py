#Author: B.A.D.R. Senarathne
#Date:2024.12.10
#Student ID: 20232126/W2120666
import csv

#Task A: Input Validation
date=0
def validate_date_input():
    "Validate the date input"
    global date
    date=0
    month=0
    year=0
    #day input
    while True:
        try:
            day=int(input("Enter the day in numbers:"))
        except ValueError:
            print("Integer required")
            continue
        if day>0 and day<=31:
            print(f"Day:{day}")
            day=str(day).zfill(2)
            break
    
        else:
            print("Out of range - value must be in the range 1 to 31.")
    #month input    
    while True:
        try:
            month=int(input("Enter the Month in numbers:"))
        except ValueError:
            print("Integer required")
            continue
        if month>0 and month<=12:
            print(f"Month:{month}")
            month=str(month).zfill(2)
            break
        else:
            print("Out of range - value must be in the range 1 to 12.")
    #year input        
    while True:
        try:
            year=int(input("Enter the year in YYYY format:"))
        except ValueError:
            print("Integer required")
            continue
        if year>=2000 and year<=2024:
            print(f"Year:{year}")
            break
        else:
            print("Out of range - value must be from 2000 and 2024.")
    # validated date output
    date=day,month,year
    date=str(date).replace("'","")
    print(f"Date:{date}")
    return

answer=0
def validate_continue_input():
    "Prompt user to decide whether to load another dataset"
    global answer
    while True:
        yes_no=input("laod another Dataset (Y/N):")
        yes_no=yes_no.upper()
        if yes_no=="Y":
            print("Continue")
            answer=yes_no
            return answer
            break
        elif yes_no=="N":
            print("Quit")
            answer=yes_no
            return answer
            break
        else:
            print("Invalid input enter Y or N")
    
        
            
#Task B: Processed Outcomes
csv_file=0
data=0
results=0
num_hours=0
def process_csv_data(file_path): 
    "Read and analyze the csv file by using the file path"
    global data
    global results
    global num_hours
    
    try:
        csv_file= open(file_path,'r')
        reader=csv.DictReader(csv_file)
        data=list(reader)

        total_vehicls=len(data)#Total number of vehicals
        
        trucks=sum(1 for row in data if row['VehicleType']=='Truck')#total number of trucks

        e_vehicles=sum(1 for row in data if row['elctricHybrid']=='True')#Total number of elctric Vehicles

        scooter=sum(1 for row in data if row['VehicleType']=='Scooter')#Total number of two Wheeled vehicles
        bicycle=sum(1 for row in data if row['VehicleType']=='Bicycle')
        motorcycle=sum(1 for row in data if row['VehicleType']=='Motorcycle')
        two_wheel=scooter+bicycle+motorcycle
        
        #total number of Buses out from elm/rabbit road 
        bus_out_elm=sum(1 for row in data if row['VehicleType']=='Buss' and row['JunctionName']=='Elm Avenue/Rabbit Road' and row['travel_Direction_out']=='N')

        no_turn=sum(1 for row in data if row['travel_Direction_in']== row['travel_Direction_out'])# Total number of vehical without turning 

        truck_percentage=(trucks/total_vehicls)*100#total truck percentage

        avg_bicycles=round(bicycle/24)# Average number of bicycles per hour
        
        over_speed=sum(1 for row in data if row['VehicleSpeed']>row['JunctionSpeedLimit'])#Total number if vehical went over the speed

        elm_rabbit=sum(1 for row in data if row['JunctionName']=='Elm Avenue/Rabbit Road')#Total number of vehicles from Elm avenue/rabbit road
        
        hanley_westway=sum(1 for row in data if row['JunctionName']=='Hanley Highway/Westway')#Total number of vehicles from hanley highway/westway

        elm_scooters=sum(1 for row in data if row['JunctionName']=='Elm Avenue/Rabbit Road' and row['VehicleType']=='Scooter')
        elm_scooter_perc=(elm_scooters/elm_rabbit)*100
        

        #calculate the peak hour
        hourly_count={}
        for row in data:
            hour=row['timeOfDay'].split(':')[0]

            if hour not in hourly_count:
                hourly_count[hour]=0
            hourly_count[hour]+=1

        peak_hour=max(hourly_count,key=hourly_count.get)
        peak_count=hourly_count[peak_hour]
        csv_file.close()
        #print(f'Number of vehicle:{peak_count}')
        #print(f'Peak Hour/s:{peak_hour}:00 - {int(peak_hour)+1}:00')
        

        #Rainy hours
        rainy_hours=set()
        for row in data:
            if row['Weather_Conditions']=='Heavy Rain' or row['Weather_Conditions']=='Light Rain':
                hour=row['timeOfDay'].split(':')[0]
                hours=int(hour)
                rainy_hours.add(hours)
                num_hours=len(rainy_hours)
       

        results=[total_vehicls,trucks, e_vehicles,two_wheel,bus_out_elm,no_turn,truck_percentage, avg_bicycles,over_speed, elm_rabbit,hanley_westway,elm_scooter_perc,peak_count,peak_hour,num_hours,file_path]
        return results
    except FileNotFoundError:
        print(f"File {file_path} not found")
    
        return results

def display_outcomes(results):
    """Display all the outcomes after analyzing and calculating the data from the CSV file"""
    print(f"File Name:{results[15]}")
    print(f"Total Vehicles: {results[0]}")
    print(f"Total number of Trucks: {results[1]}")
    print(f"Total number of Electric Vehicles: {results[2]}")
    print(f"Total number of Two-Wheeled Vehicles: {results[3]}")
    print(f"Buses Out from Elm North: {results[4]}")
    print(f"Vehicles went without turning: {results[5]}")
    print(f"Truck Percentage: {round(results[6])}%")
    print(f"Average Bicycles per Hour: {results[7]}")
    print(f"Vehicles Over Speed Limit: {results[8]}")
    print(f"Total Vehicles from Elm Avenue/Rabbit Road: {results[9]}")
    print(f"Total Vehicles from Hanley Highway/Westway: {results[10]}")
    print(f"Scooters in Elm Avenue/Rabbit Road: {round(results[11])}%")
    print(f"number of vehicles in the Peak hour: {results[12]}")
    print(f"Peak Hours: {results[13]}:00 - {int(results[13]) + 1}:00")
    print(f"Rainy Hours: {results[14]}")
    return


def save_results_to_file(results,file_name="results.txt"):
    "Write the csv file calculation to a text file and append if the program loops"
    file=open("results.txt","a")    
    file.write(f"File Name:{results[15]}\n")
    file.write(f"Total number of Vehicles: {results[0]}\n")
    file.write(f"Total number of Trucks: {results[1]}\n")
    file.write(f"Total number of Electric Vehicles: {results[2]}\n")
    file.write(f"Total number of Two-Wheeled Vehicles: {results[3]}\n")
    file.write(f"Total number of Buses Out from Elm North: {results[4]}\n")
    file.write(f"Total number of vehicles passing without turning: {results[5]}\n")
    file.write(f"Truck Percentage on the selected date: {round(results[6])}%\n")
    file.write(f"Average Bicycles per Hour: {results[7]}\n")
    file.write(f"Total number of vehicles recorded as Over Speed Limit: {results[8]}\n")
    file.write(f"Total Vehicles from Elm Avenue/Rabbit Road: {results[9]}\n")
    file.write(f"Total Vehicles from Hanley Highway/Westway: {results[10]}\n")
    file.write(f"Total number of Scooters in Elm Avenue/Rabbit Road: {round(results[11])}%\n")
    file.write(f"Number of vehicles recorded in the Peak hour in Hanley Highway/westway: {results[12]}\n")
    file.write(f"Peak hours in Hanley Highway/westway: {results[13]}:00 - {int(results[13]) + 1}:00\n")
    file.write(f"Total number of Rainy Hours on the selected date: {results[14]}\n")
    file.write('\n'+'*'*10 +'\n')
    return

if __name__=="__main__":
    
    while True:
        #calling funtions
        validate_date_input()
        #validate_continue_input()

        #file path
        file_date=str(date).strip("()").replace(", ","")
        file_date=file_date+".csv"
        file_name="traffic_data"+file_date
        #print(f"File name:{file_name}")
        file_path=file_name


        #Calling funtion
        process_csv_data(file_path)
        print("  ")
        if results==0:
            validate_continue_input()
            if answer=="N":
                break
            else:
                continue
        else:          
            display_outcomes(results)

            save_results_to_file(results,file_name="results.txt")
            validate_continue_input()
            if answer=="Y":
                continue
            else:
                break


