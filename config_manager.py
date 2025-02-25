from cryptography.fernet import Fernet
import json

class Config_Manager:
  def __init__(self):
    self.key = None
    self.load_key()

  def load_key(self):
    try:
      with open("master.key", "rb") as key_file:
        key = key_file.read()
        self.key = Fernet(key)
    except (FileNotFoundError):
      print(f"There is no {filepath} found. Please add the key file")

  def create_config(self, config_json):
    return json.dumps(config_json)

  def encrypt(self):
    try:
      config_json = self.create_config().encode()
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
      print(decrypted_config.decode())
    except Exception as e:
      print(f"An error occurred while decrypting the file {e}")


if __name__ == "__main__":
  Encryptor().encrypt()