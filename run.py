from config_manager import Config_Manager

def main():
  if not file_exists('config.json.enc'):
    config_setup()
  if not file_exists('master.key'):
    master_key_setup()

  config = Config_Manager()
  config.load_config()

  match config.pos_type:
    case 'printer':
      printer_interface()
    case 'pos':
      pos_interface()
    case 'kiosk':
      kiosk_interface()
    case 'order_screen':
      order_screen_interface()
    case 'order_pickup':
      order_pickup_interface()
    case _:
      raise Exception(f"Unknown POS type: {config.pos_type}")

def config_setup():
  pass

def master_key_setup():
  pass

def printer_interface():
  pass

def pos_interface():
  pass

def kiosk_interface():
  pass

def order_screen_interface():
  pass

def order_pickup_interface():
  pass

def file_exists(file):
  try:
    with open(file, 'r') as f:
      return True
  except FileNotFoundError:
    return False

if __name__ == '__main__':
  main()