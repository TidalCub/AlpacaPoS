import paho.mqtt.client as mqtt
import os
from config_manager import Config_Manager

def load_config():
  cm = Config_Manager()
  cm.load_config()
  return cm.host, int(cm.port), "printer", cm.username, cm.password

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to MQTT broker")
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Message received: {message}")
    try:
        os.system(f'echo "{message}" > /dev/usb/lp0')
    except Exception as e:
        print(f"Error writing to printer: {e}")

if __name__ == "__main__":
    MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, MQTT_USERNAME, MQTT_PASSWORD = load_config()
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        print(f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_forever()
    except Exception as e:
        print(f"Connection failed: {e}")