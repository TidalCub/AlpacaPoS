import paho.mqtt.client as mqtt
import os
from config_manager import Config_Manager
import json

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
      receipt = format_receipt(message)
      os.system(f'echo "{receipt}" > /dev/usb/lp0')
    except Exception as e:
      print(f"Error writing to printer: {e}")

def format_receipt(payload):
    data = json.loads(payload)
    receipt_lines = []

    # Add store name centered
    receipt_lines.append("\x1B\x61\x01" + data['order_details']['store'] + "\x1B\x61\x00")  # Center text
    receipt_lines.append("\n")

    # Add order ID
    receipt_lines.append(f"Order ID: {data['order_id']}")
    receipt_lines.append("\n")

    # Add items
    receipt_lines.append("Items:")
    receipt_lines.append("\n")
    for item in data['items']:
        receipt_lines.append(f"{item['name']} x{item['quantity']} @ ${item['price']:.2f}")
        receipt_lines.append("\n")

    # Add total
    receipt_lines.append("\n")
    receipt_lines.append(f"Total: ${data['total']:.2f}")
    receipt_lines.append("\n")

    # Add order details
    receipt_lines.append("\n")
    receipt_lines.append(f"Started at: {data['order_details']['started_at_time']}")
    receipt_lines.append("\n")
    receipt_lines.append(f"Last updated at: {data['order_details']['last_updated_at_time']}")
    receipt_lines.append("\n")

    # Add cut command
    receipt_lines.append("\x1D\x56\x42\x00")  # Cut paper

    return ''.join(receipt_lines)

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