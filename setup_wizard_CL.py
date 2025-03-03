import json
import socket
import paho.mqtt.client as mqtt
from config_manager import Config_Manager

CONFIG_FILE = "config.json"

def get_input(prompt, default=""):
    value = input(f"{prompt} [{default}]: ").strip()
    return value if value else default

def test_mqtt_connection(host, port, username="", password=""):
    client = mqtt.Client()
    client.username_pw_set(username, password)

    try:
        client.connect(host, int(port), 60)
        client.loop_start()
        print("Connection successful!")
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

def setup_wizard():
    print("Welcome to the Setup Wizard!\n")

    # Step 1: Get MQTT Configuration
    host = get_input("Enter MQTT Host", "localhost")
    port = get_input("Enter MQTT Port", "1883")
    username = get_input("Enter MQTT Username", "")
    password = get_input("Enter MQTT Password", "")

    # Step 2: Test Connection
    if not test_mqtt_connection(host, port):
        print("Warning: Connection failed, but continuing...\n")

    # Step 3: Select Device Type
    device_types = ["Printer", "POS Terminal", "Order Screen", "Kitchen Display", "Kiosk"]
    
    print("\nSelect a device type:")
    for i, device in enumerate(device_types, 1):
        print(f"{i}. {device}")

    while True:
        choice = input("\nEnter choice (1-5): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(device_types):
            device_type = device_types[int(choice) - 1]
            break
        print("Invalid choice, try again.")

    # Step 4: Save Configuration
    config = {
        "authentication": {"username": username, "password": password},
        "MQTT_BROKER": {"host": host, "port": port},
        "device_type": device_type,
    }

    cm = Config_Manager()
    cm.encrypt(config)

    print("\nConfiguration saved successfully in 'config.json.enc'. Setup complete!\n")

if __name__ == "__main__":
    setup_wizard()