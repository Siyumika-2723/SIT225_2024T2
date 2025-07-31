import serial
from datetime import datetime


ser = serial.Serial('COM3', 9600)
filename = "dht22_data.csv"

print("Starting data logging... Press Ctrl+C to stop.")

with open(filename, "a") as file:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            file.write(f"{timestamp},{line}\n")
            print(f"{timestamp},{line}")
