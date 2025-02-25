import json
from cryptography.fernet import Fernet
import os

class Config:
  def __init__(self):
    self.host = "localhost"
    self.port = 1883
    self.username = None
    self.password = None
    self.load_config() 

  def load_config(self):
    try:
      with open('config.json', 'r') as f:
        config = json.load(f)
        self.host = str(config['MQTT_BROKER']['host'])
        self.port = int(config['MQTT_BROKER']['port'])

    except (FileNotFoundError, json.JSONDecodeError) as e:
      print(f"There is no {filepath} found. Defaulting to defaults")