import serial
import time
from datetime import datetime


arduino_port = 'COM3'
baud_rate = 9600
file_name = "hcsr04_data.csv"


ser = serial.Serial(arduino_port, baud_rate)
print(f"Connected to {arduino_port}")


with open(file_name, "a") as file:
    while True:
        try:
            data = ser.readline().decode().strip()
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            if data:  
                print(f"{timestamp},{data}")
                file.write(f"{timestamp},{data}\n")
                file.flush()
        except KeyboardInterrupt:
            print("Data collection stopped by user.")
            break
        except Exception as e:
            print(f"Error: {e}")
