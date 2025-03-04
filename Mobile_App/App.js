import React, { useEffect } from 'react';
import { Text, View, Alert, StyleSheet } from 'react-native';
import mqtt from 'react-native-mqtt';

export default function App() {
  useEffect(() => {
    // Replace YOUR_PI_IP with the actual IP address of your Raspberry Pi
    const client = mqtt.connect('mqtt://YOUR_PI_IP:1883');

    client.on('connect', () => {
      client.subscribe('environment/alerts');
    });

    client.on('message', (topic, message) => {
      const payload = JSON.parse(message.toString());
      if (topic === 'environment/alerts') {
        Alert.alert(
          'Environment Alert!',
          `Temperature: ${payload.temperature}°C\nHumidity: ${payload.humidity}%`,
          [{ text: 'OK' }]
        );
      }
    });

    // Clean up on unmount
    return () => client.end();
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.text}>IoT Safety Monitoring Mobile App</Text>
      <Text style={styles.text}>Waiting for alerts...</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1, 
    justifyContent: 'center', 
    alignItems: 'center'
  },
  text: {
    fontSize: 18,
    margin: 10
  }
});
