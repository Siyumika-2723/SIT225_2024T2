import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


file_path = "DHT22_data.csv"  
df = pd.read_csv(file_path, names=["timestamp", "temperature", "humidity"])


df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y%m%d%H%M%S", errors='coerce')


df["temperature"] = pd.to_numeric(df["temperature"], errors='coerce')
df["humidity"] = pd.to_numeric(df["humidity"], errors='coerce')
df.dropna(inplace=True)  


plt.figure(figsize=(12, 6))
plt.plot(df["timestamp"], df["temperature"], label="Temperature (°C)", color="orange", linewidth=2)
plt.plot(df["timestamp"], df["humidity"], label="Humidity (%)", color="blue", linewidth=2)


plt.title("DHT22 Sensor Data: Temperature and Humidity Over Time")
plt.xlabel("Timestamp")
plt.ylabel("Values")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()


plt.savefig("dht22_plot.png")  
plt.show()
