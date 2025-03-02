from cryptography.fernet import Fernet
import json

class Config_Manager:
  def __init__(self):
    self.key = None
    self.load_key()
    self.host = "localhost"
    self.port = 1883
    self.username = "None"
    self.password = "None"
    self.pos_type = "printer"
    self.config = None

  def load_key(self):
    try:
      with open("master.key", "rb") as key_file:
        key = key_file.read()
        self.key = Fernet(key)
    except (FileNotFoundError):
      print(f"There is no {filepath} found. Please add the key file")

  def create_config(self, config_json):
    self.config
    return json.dumps(config_json)

  def encrypt(self, config):
    try:
      config_json = self.create_config(config).encode()
      encrypted_config = self.key.encrypt(config_json)
      with open("config.json.enc", "wb") as enc_file:
        enc_file.write(encrypted_config)
      print("File encrypted successfully")
    except Exception as e:
      print(f"An error occurred while encrypting the file {e}")

  def decrypt(self):
    try:
      with open("config.json.enc", "rb") as enc_file:
        encrypted_config = enc_file.read()
      decrypted_config = self.key.decrypt(encrypted_config)
      return decrypted_config.decode()
    except Exception as e:
      print(f"An error occurred while decrypting the file {e}")

  def load_config(self):
    try:
      decrypted_config = self.decrypt()
      data = json.loads(decrypted_config)
      self.host = str(data['MQTT_BROKER']['host'])
      self.port = int(data['MQTT_BROKER']['port'])
      self.username = str(data['authentication']['username'])
      self.password = str(data['authentication']['password'])
      return True
    except Exception as e:
      print(f"An error occurred while loading the config {e}")

if __name__ == "__main__":
  Config_Manager().decrypt()