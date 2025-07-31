import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("dht22_data.csv", header=None, names=["timestamp", "temperature", "humidity"])


df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y%m%d%H%M%S")


plt.figure(figsize=(10, 5))
plt.plot(df["timestamp"], df["temperature"], label="Temperature (°C)", color="red")
plt.plot(df["timestamp"], df["humidity"], label="Humidity (%)", color="blue")
plt.xlabel("Time")
plt.ylabel("Values")
plt.title("DHT22 Sensor Data Over Time")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("dht22_plot.png")  
plt.show()  
