# SIT225_2024T2

This repository contains coursework for SIT225 2024 Trimester 2.

## Structure

- `week-1/` - Week 1 materials and assignments
- `week-2/` - Week 2 materials and assignments
  - DHT22 Temperature/Humidity Sensor Project
  - HC-SR04 Ultrasonic Distance Sensor Project

## Week 2 - HC-SR04 Ultrasonic Sensor Data Logger Project

This project demonstrates real-time data logging from an HC-SR04 ultrasonic sensor connected to an Arduino, with data visualization using Python.

### Files Description

- `hcsr04_logger.py` - Main Python script that reads distance data from Arduino via serial communication and logs it to a CSV file
- `plot.py` - Python script to visualize the logged distance data over time
- `hcsr04_data.csv` - CSV file containing timestamped distance measurements

### Hardware Setup

- Arduino board (Uno/Nano/etc.)
- HC-SR04 Ultrasonic Sensor
- USB cable for serial communication

### Software Requirements

```bash
pip install pyserial pandas matplotlib
```

### Usage

1. **Data Collection**: Run the logger to start collecting data from the sensor
   ```bash
   python hcsr04_logger.py
   ```

2. **Data Visualization**: Generate a plot of the collected data
   ```bash
   python plot.py
   ```

### Features

- Real-time data logging with timestamps
- Serial communication with Arduino
- CSV data storage
- Time-series visualization
- Error handling and graceful shutdown

### Arduino Code

Make sure your Arduino is programmed to send distance readings from the HC-SR04 sensor over serial communication at 9600 baud rate.

### Configuration

- Default COM port: `COM3`
- Baud rate: `9600`
- Output file: `hcsr04_data.csv`

Modify the `arduino_port` variable in `hcsr04_logger.py` if your Arduino is connected to a different port.
