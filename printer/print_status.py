import socket
import subprocess
from escpos.printer import Usb

def ip():
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip
  except Exception:
      return "Unknown"

def check_internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return "Connected"
    except Exception:
        return False

def main():
  p = Usb(0x04b8, 0x0202)
  p.text("Checking Internet Status\n")
  p.text("Status: " + check_internet())
  p.text("\u2500" * 32 + "\n")
  p.text("Ip Address of Device: " + ip())