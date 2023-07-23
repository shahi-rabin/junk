import requests
import json
import paho.mqtt.client as mqtt

# Replace with your actual Firebase Realtime Database URL
database_url = "https://your-project-id.firebaseio.com"

# Replace with your actual API key
api_key = "your-api-key"

# Endpoint to access the Firebase Realtime Database
url = f"{database_url}/.json?auth={api_key}"

# Replace with your ThingsBoard MQTT broker and access token
thingsboard_broker = "localhost"  # Use "localhost" if running on the same machine
access_token = "YOUR_ACCESS_TOKEN"

# MQTT topic to send telemetry data
mqtt_topic = f"v1/devices/me/telemetry"

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker with result code " + str(rc))

try:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.username_pw_set(access_token)
    client.connect(thingsboard_broker, 1883, 60)
    client.loop_start()

    while True:
        response = requests.get(url)
        data = response.json()
        print(data)

        # Send the data to ThingsBoard via MQTT
        client.publish(mqtt_topic, json.dumps(data))
        print("Data sent to ThingsBoard via MQTT.")

        time.sleep(5)  # Adjust the interval (in seconds) between requests

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
    print("Script interrupted.")
