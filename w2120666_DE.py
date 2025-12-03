#Author: B.A.D.R. Senarathne
#Date:2024.12.24
#Student ID: 20232126/W2120666
import w2120666_ABC as code1

#Task D
import tkinter as tk

class HistogramApp:
    def __init__(self, results, date):
        'Initializes the histogram application with the traffic data and selected date.'

        self.traffic_data = results
        self.date = date
        self.root = tk.Tk()
        self.root.title("Histogram")
        self.canvas = tk.Canvas(self.root, width=1250, height=525, bg="white")
        self.canvas.pack()
        

    def setup_window(self):
        'Sets up the Tkinter window and canvas for the histogram.'
        #x axis
        self.canvas.create_line(50,450,1170,450, width=6)

        #Label for X axis
        self.canvas.create_text(650, 500, text="Hours 00:00 to 24:00", font=("Times Roman", 12,'bold'))
        

    def draw_histogram(self):
        'Draws the histogram with axes, labels, and bars.'
        #setting hours count 24    
        hourly_counts = {hour: [0, 0] for hour in range(24)}  

        #Process  traffic_data
        #Data of Elm Avenue/Rabbit road
        for hour, entry in self.traffic_data[0].items():
            hour = int(hour)  
            if hour in hourly_counts:
                hourly_counts[hour][0] += entry
        #Data of Hanley highway/Westway        
        for hour, entry in self.traffic_data[1].items():
            hour = int(hour)
            if hour in hourly_counts:
                hourly_counts[hour][1] += entry

        #Extract data 
        hours = list(hourly_counts.keys()) #hours list
        elm_counts = [hourly_counts[hour][0] for hour in hours] #Elm Avenue/Rabbit road vehicle count
        hanley_counts = [hourly_counts[hour][1] for hour in hours] #Hanley Highway/Westway vehicle count

        #scaling the histogram
        max_count = max(max(elm_counts), max(hanley_counts)) #maximum vehicle counts
        bar_width = 20 #bar width
        spacing = 5 # space between bars
        offset_x = 70 #Horizontal offset of bars
        offset_y = 450 #Vertical line of Histogram
        scaling_factor = 350 / max_count #scale the bars to the canvas

        #data iteration 
        i=0
        for hour in hours:
            #Elm Avenue/Rabbit Road bars
            x1 = offset_x + i * (bar_width * 2 + spacing) #left x coordinate for bars
            y1 = offset_y - elm_counts[i] * scaling_factor # max y coordinate for bars
            x2 = x1 + bar_width #right x coordinate for bars
            self.canvas.create_rectangle(x1, y1, x2, offset_y, fill="lightgreen", outline="black")
            self.canvas.create_text(x1 + bar_width / 2, y1 - 10, text=str(elm_counts[i]), font=("Times roman", 8), fill="green")

            #Hanley Highway/Westway bars 
            x1 = x2 + spacing #Bar spacing for x coordinate
            y1 = offset_y - hanley_counts[i] * scaling_factor #max y coordinate for bars
            x2 = x1 + bar_width #rigth x coordinates for bars
            self.canvas.create_rectangle(x1, y1, x2, offset_y, fill="lightcoral", outline="black")
            self.canvas.create_text(x1 + bar_width / 2, y1 - 10, text=str(hanley_counts[i]), font=("Times roman", 8), fill="red")

            #x axis labels
            self.canvas.create_text((x1 + x2) / 2, offset_y + 20, text=str(hour), font=("Times roman", 8))

            i+=1


    def add_legend(self):
        'Adds a legend to the histogram to indicate which bar corresponds to which junction.'
            
        legend_x = 50
        legend_y = 20

        #Histogram Title
        self.canvas.create_text(legend_x + 10, legend_y + 3, text=f"Histogram of Vehicle Frequency per Hour {self.date}", anchor="nw", font=("Times roman", 14, "bold"))

        #Lengends of Elm Avenue/Rabbit Road
        self.canvas.create_rectangle(legend_x + 10, legend_y + 30, legend_x + 30, legend_y + 50, fill="lightgreen", outline="black")#Elm Avenue/Rabbit Road
        self.canvas.create_text(legend_x + 40, legend_y + 40, text="Elm Avenue/Rabbit Road", anchor="w", font=("Times roman", 10))

        #Legends of Hanley Highway/Westway
        self.canvas.create_rectangle(legend_x + 10, legend_y + 60, legend_x + 30, legend_y + 80, fill="lightcoral", outline="black")#Hanley Highway/Westway
        self.canvas.create_text(legend_x + 40, legend_y + 70, text="Hanley Highway/Westway", anchor="w", font=("Times roman", 10))

            
        
    def run(self):
        'Runs the Tkinter main loop to display the histogram.'

        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        self.root.mainloop()


#Task E
class MultiCSVProcessor:
    def __init__(self):
        'Initializes the application for processing multiple CSV files.'
        self.current_data =[]
        self.file_path = None

        
    def clear_previous_data(self):
        'Clears data from the previous run to process a new dataset.'
        self.current_data = None
        self.file_path = None
        
    def load_csv_data(self):
        'Loads a CSV file and processes its data.'
        file=open(self.file_path, 'r')
        lines=file.readlines() 
        self.current_data=[i.strip().split(',') for i in lines[1:]]
        file.close()

    def handle_user_interaction(self):
        'Handles user input for processing multiple files.'
        try:
            code1.validate_date_input()#validate the user date input
            code1.file_date=str(code1.date).strip("()").replace(", ","")#convert the date as file name
            file_date=code1.file_date+".csv" 
            self.file_path="traffic_data"+file_date 
            code1.process_csv_data(self.file_path) #Process csv file 
            ##code1.display_outcomes(code1.results) 
            self.load_csv_data() #csv file handling
            self.process_files() #Process csv data
            self.user_date=code1.date #Store date
        except TypeError:
            print(f'file not found ({self.file_path})') #Error handling
                    
    def process_files(self):
        'Main loop for handling multiple CSV files until the user decides to quit.'
        print("Histogram Displayed \nClose Histogram to continue")
        hourly_count_hanley = {f"{hour:02d}":0 for hour in range(24)} #Count of Hanley Highway/Westway
        hourly_count_rabbit = {f"{hour:02d}":0 for hour in range(24)} #Count of Elm Avenue/Rabbit Road
        for row in self.current_data:
            # Update hourly count

            #Hanley Highway/Westway
            if row[0]=='Hanley Highway/Westway':
                hour = row[2].split(':')[0] # Extract count hours
                hour=f"{int(hour):02d}" #set to 2 digits
                if hour in hourly_count_hanley:
                    hourly_count_hanley[hour] += 1 #count update

            #Elm Avenue/Rabbit Road
            else:
                hour = row[2].split(':')[0] #Extract count hours
                hour=f"{int(hour):02d}" #set to 2 digits
                if hour in hourly_count_rabbit:
                    hourly_count_rabbit[hour] += 1 #Count update

        #storeing date       
        self.current_data.clear()
        self.current_data.append(hourly_count_hanley)#Hanley Highway/Westway count
        self.current_data.append(hourly_count_rabbit)#Elm Avenue/Rabbit Road count
    


if __name__ == "__main__":
    while True:
        try:
            processor = MultiCSVProcessor() #Initialize data
            processor.handle_user_interaction() #Handle user interactions and file processing
      
            if processor.current_data:
                app = HistogramApp(processor.current_data,date=processor.user_date)
                app.run() #Display Histogram
                
            #Taking user inputs to the loop    
            while True:  
                loop=input("Do you want to load a another data file (Y/N):")
                loop=loop.upper()
        
                if loop=='N':
                    print('Quit program')
                    exit()
                elif loop=='Y':
                    print('Load another file')
                    break
                else:
                    print('Invalid Input,try again')
        
            
        except (AttributeError,NameError,FileNotFoundError):
            print("Error, Try again")
            continue

##Reference
##https://www.w3schools.com/python/default.asp
##https://docs.python.org/3/library/tkinter.html
##https://youtu.be/lyoyTlltFVU?si=QTQUUPVvKpWvqcW9



