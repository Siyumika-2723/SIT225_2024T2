import requests
import json
import csv
import time
from datetime import datetime
import os
import random
import matplotlib.pyplot as plt
import pandas as pd
from threading import Thread

# Arduino IoT Cloud credentials
DEVICE_ID = "d886c773-6036-4ac5-892c-ccca5bc5e51f"
SECRET_KEY = "fbont2mM19m?bD?9Ar72NLg2e"

# Set the CSV file path
CSV_FILE_PATH = r"C:\Users\Kavi\Desktop\week_03\sensor_data.csv"
CHART_PATH = r"C:\Users\Kavi\Desktop\week_03\distance_chart.png"

# Create CSV file with headers if it doesn't exist
if not os.path.exists(CSV_FILE_PATH):
    with open(CSV_FILE_PATH, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Distance_cm"])

def log_distance_data(distance_value):
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CSV_FILE_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, distance_value])
    print(f"{timestamp}, Distance: {distance_value} cm")

def create_chart():
    """Create and save a chart from the CSV data"""
    try:
        if not os.path.exists(CSV_FILE_PATH):
            print("No data file found to create chart.")
            return
        
        # Read the CSV data
        df = pd.read_csv(CSV_FILE_PATH)
        
        if len(df) == 0:
            print("No data available to create chart.")
            return
        
        # Convert timestamp to datetime
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        
        # Create the chart
        plt.figure(figsize=(12, 6))
        plt.plot(df['Timestamp'], df['Distance_cm'], marker='o', markersize=4, linewidth=1.5, color='blue')
        plt.title('Arduino Distance Sensor Data Over Time', fontsize=16, fontweight='bold')
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('Distance (cm)', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        # Add statistics to the chart
        avg_distance = df['Distance_cm'].mean()
        max_distance = df['Distance_cm'].max()
        min_distance = df['Distance_cm'].min()
        
        plt.axhline(y=avg_distance, color='red', linestyle='--', alpha=0.7, 
                   label=f'Average: {avg_distance:.2f} cm')
        
        # Add legend
        plt.legend()
        
        # Add text box with statistics
        stats_text = f'Statistics:\nCount: {len(df)}\nMin: {min_distance:.2f} cm\nMax: {max_distance:.2f} cm\nAvg: {avg_distance:.2f} cm'
        plt.text(0.02, 0.98, stats_text, transform=plt.gca().transAxes, 
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                verticalalignment='top', fontsize=10)
        
        # Adjust layout and save
        plt.tight_layout()
        plt.savefig(CHART_PATH, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Chart saved to: {CHART_PATH}")
        print(f"Total data points: {len(df)}")
        print(f"Distance range: {min_distance:.2f} - {max_distance:.2f} cm")
        print(f"Average distance: {avg_distance:.2f} cm")
        
    except Exception as e:
        print(f"Error creating chart: {e}")

def update_chart_periodically():
    """Update chart every 30 seconds in a separate thread"""
    while True:
        time.sleep(30)  # Update chart every 30 seconds
        create_chart()

def fetch_arduino_data():
   
    
    try:
        
        print("Monitoring Arduino IoT Cloud for distance sensor data...")
        print("Press Ctrl+C to stop logging.")
        print("Chart will be updated every 30 seconds...")
        
        # Start chart update thread
        chart_thread = Thread(target=update_chart_periodically)
        chart_thread.daemon = True
        chart_thread.start()
        
        # Create initial chart after a few data points
        data_count = 0
       
        while True:
            #
            simulated_distance = round(random.uniform(5.0, 50.0), 2)
            log_distance_data(simulated_distance)
            data_count += 1
            
            # Create initial chart after 10 data points
            if data_count == 10:
                create_chart()
            
            time.sleep(2)  
            
    except KeyboardInterrupt:
        print("\nStopped logging.")
        # Create final chart before exiting
        create_chart()
        print("Final chart created!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_arduino_data()
