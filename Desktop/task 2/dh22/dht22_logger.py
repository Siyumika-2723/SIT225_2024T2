import serial
import time
from datetime import datetime


ser = serial.Serial('COM3', 9600) 
sensor_filename = "DHT22_data.csv"

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line:
                
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                
                
                data_line = f"{timestamp},{line}"
                
                
                with open(sensor_filename, "a") as file:
                    file.write(data_line + "\n")
                
                print(data_line)

except KeyboardInterrupt:
    print("\nData collection stopped by user.")

finally:
    ser.close()

