from flask import Flask, render_template
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt
import sqlite3
import json
import logging

app = Flask(__name__)
socketio = SocketIO(app)

# Setup logging
logging.basicConfig(level=logging.INFO)

# Database setup (SQLite)
conn = sqlite3.connect('sensor_data.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS sensor_data
             (timestamp DATETIME, temperature REAL, humidity REAL)''')

def on_connect(client, userdata, flags, rc):
    logging.info("Connected to MQTT Broker with result code " + str(rc))
    client.subscribe("environment/#")

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    if msg.topic == 'environment/data':
        # Store data in the database
        c.execute("INSERT INTO sensor_data VALUES (datetime('now'), ?, ?)",
                  (data['temperature'], data['humidity']))
        conn.commit()
        # Emit update to dashboard
        socketio.emit('update', data)
    elif msg.topic == 'environment/alerts':
        socketio.emit('alert', data)
        logging.warning("Alert received: " + str(data))

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

@app.route('/')
def index():
    return render_template('dashboard.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
