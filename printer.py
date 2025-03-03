import paho.mqtt.client as mqtt
import json
from escpos.printer import Usb
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
        receipt = format_receipt(message)
        print_receipt(receipt)
    except Exception as e:
        print(f"Error writing to printer: {e}")

def format_receipt(payload):
    data = json.loads(payload)
    p = Usb(0x04b8, 0x0202)  # Vendor & Product ID for Epson TM-T70
    
    # Store name (centered & bold)
    p.set(align='center', bold=True, height=2, width=2)
    p.text(data['order_details']['store'] + "\n")
    p.set(bold=False, height=1, width=1)
    p.text("\n")
    
    # Order ID
    p.set(align='left')
    p.text(f"Order ID: {data['order_id']}\n")
    p.text("\n")
    
    # Items
    p.set(align='center', bold=True, height=2, width=2)
    p.text("Items:\n")
    p.text("\u2500" * 32 + "\n")
    p.set(align='left', bold=False, height=1, width=1)
    for item in data['items']:
      name = item['name']
      quantity = 1
      price = float(item['price'])
      p.text(f"{name} x{quantity} @ ${price:.2f}\n")
      for modifier in item['modifiers']:
        p.text(f" + {modifier['name']} {modifier['ingredient_group']}\n")

    p.set(align='center', bold=True, height=2, width=2)
    p.text("\u2500" * 32 + "\n")
    p.set(align='left', bold=False, height=1, width=1)

    # Total
    total = float(data['total'])
    p.text("\n")
    p.set(bold=True)
    p.text(f"Total: ${total:.2f}\n")
    p.set(bold=False)
    p.text("\n")
    
    # Order details
    p.text(f"Started at: {data['order_details']['started_at_time']}\n")
    p.text(f"Last updated at: {data['order_details']['last_updated_at_time']}\n")
    
    # Cut paper
    p.cut()
    
    return p

def print_receipt(printer):
    try:
        printer.close()
    except Exception as e:
        print(f"Error closing printer: {e}")

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
