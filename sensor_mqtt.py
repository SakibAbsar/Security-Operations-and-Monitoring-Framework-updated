"""
IoT Environmental Sensor Data Collector
Author: [Sakib Absar]
"""

import Adafruit_DHT
import paho.mqtt.client as mqtt
import time
import json
import logging

# Configuration
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
MQTT_BROKER = 'localhost'
MQTT_TOPIC_DATA = 'environment/data'
MQTT_TOPIC_ALERT = 'environment/alerts'
TEMP_THRESHOLD = 40  # °C
HUM_THRESHOLD = 80   # %

# Initialize logging
logging.basicConfig(level=logging.INFO)

def connect_mqtt():
    """Initialize and connect MQTT client."""
    client = mqtt.Client()
    try:
        client.connect(MQTT_BROKER, 1883, 60)
        logging.info("Connected to MQTT Broker")
        return client
    except Exception as e:
        logging.error(f"MQTT Connection Error: {str(e)}")
        exit(1)

def read_sensor():
    """Read data from the DHT11 sensor."""
    humidity, temp = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is None or temp is None:
        logging.warning("Sensor read failed. Retrying...")
        return None, None
    return humidity, temp

def main():
    client = connect_mqtt()
    
    while True:
        humidity, temp = read_sensor()
        if humidity is not None and temp is not None:
            payload = {
                'temperature': temp,
                'humidity': humidity,
                'alert': False
            }
            
            # Check alert thresholds
            if temp > TEMP_THRESHOLD or humidity > HUM_THRESHOLD:
                payload['alert'] = True
                client.publish(MQTT_TOPIC_ALERT, json.dumps(payload))
                logging.warning("Alert triggered!")
            
            client.publish(MQTT_TOPIC_DATA, json.dumps(payload))
            logging.info(f"Published: {payload}")
        time.sleep(30)

if __name__ == '__main__':
    main()
