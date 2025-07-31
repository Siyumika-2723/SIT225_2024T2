import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


df = pd.read_csv("dht22_data.csv", header=None, names=["timestamp", "temperature", "humidity"])


df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y%m%d%H%M%S")


fig, ax1 = plt.subplots(figsize=(12, 6))


color_temp = 'tab:red'
ax1.set_xlabel('Time', fontsize=12)
ax1.set_ylabel('Temperature (°C)', color=color_temp, fontsize=12)
line1 = ax1.plot(df["timestamp"], df["temperature"], 
                 color=color_temp, linewidth=2, linestyle='-', 
                 label="Temperature (°C)", marker='o', markersize=3, alpha=0.8)
ax1.tick_params(axis='y', labelcolor=color_temp)
ax1.grid(True, alpha=0.3)


ax2 = ax1.twinx()
color_hum = 'tab:blue'
ax2.set_ylabel('Humidity (%)', color=color_hum, fontsize=12)
line2 = ax2.plot(df["timestamp"], df["humidity"], 
                 color=color_hum, linewidth=2, linestyle='--', 
                 label="Humidity (%)", marker='s', markersize=3, alpha=0.8)
ax2.tick_params(axis='y', labelcolor=color_hum)


ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
ax1.xaxis.set_major_locator(mdates.HourLocator(interval=2))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)


plt.title("DHT22 Sensor Data Over Time", fontsize=14, fontweight='bold', pad=20)


lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', framealpha=0.9)


fig.tight_layout()


plt.savefig("dht22_plot.png", dpi=300, bbox_inches='tight')  
plt.show()  
