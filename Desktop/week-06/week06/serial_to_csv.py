import serial, csv, time

PORT = "COM3"         
BAUD = 115200
OUTFILE = "gyroscope.csv"
DURATION_SECONDS = 10 * 60  

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)  

with open(OUTFILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp_ms", "x", "y", "z"])  # header
    start = time.time()
    try:
        while time.time() - start < DURATION_SECONDS:
            line = ser.readline().decode("utf-8", errors="ignore").strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) >= 4:
                writer.writerow(parts[:4])
    except KeyboardInterrupt:
        print("Stopped by user")
    finally:
        ser.close()

print(f"Data saved to {OUTFILE}")
