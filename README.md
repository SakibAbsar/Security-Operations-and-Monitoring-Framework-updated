# Security-Operations-and-Monitoring-Framework-updated
# IoT Environmental Safety System

## 1. Introduction
This project demonstrates a portable IoT-enabled safety device using a Raspberry Pi and sensors to monitor environmental conditions (temperature and humidity). It features a real-time alert system via MQTT and a mobile app for instant notifications.

## 2. Technical Overview
- **Hardware:** Raspberry Pi, DHT11 sensor, pull-up resistor, jumper wires.
- **Software:** Python (sensor reading, MQTT communication, Flask dashboard), React Native (mobile notifications).
- **Communication:** MQTT protocol (using Mosquitto broker).

## 3. System Architecture
- **Data Flow:**  
  Sensor (DHT11) → Raspberry Pi (sensor_mqtt.py) → MQTT Broker (Mosquitto) → Flask Dashboard (dashboard.py) & Mobile App (React Native).


## 4. Implementation Details
- **Sensor Data Collection:** Runs every 30 seconds.
- **Alert Conditions:** Temperature > 40°C or Humidity > 80%.
- **Data Storage:** SQLite database used by the dashboard.
- **Real-time Updates:** Flask-SocketIO for live dashboard updates.

## 5. Testing & Results
- Continuous operation test for 72 hours.
- Alert latency measured at < 2 seconds.
- Accuracy: ±2°C for temperature and ±5% for humidity.

## 6. Conclusion & Future Work
This system proves the viability of low-cost IoT solutions for environmental monitoring. Future enhancements include TLS for MQTT, OTA updates, and additional sensors.

## 7. References
