# Alpaca PoS

A lightweight python based Point of Sale system to use with [Alpaca Cafe](https://github.com/TidalCub/Alpaca-Cafe).

> ## Disclaimer
>
> This is a Dissertation Project that comes with no guarantee or warranty

This project uses Python Flask on a localhost to provide a interface for use, and connects with the server via MQTT.

Current Use Case Plan:

- PoS Terminal
- Kiosk
- Receipt Printer
- Staff Order Screens
- Order Collection Screens

## Installation / Use

**This is not intended to be use and is WIP**

Alpaca PoS is for use on a linux based operating system.

You will need a master key in the `mater.key` file to decrypt `config.json.enc`. 


If you don't have the master key or config, you can create a new one. Generate a master key in `master.key`. Then:

```python

from config_manager import Config_Manager

config_as_json = #Make the new config in a JSON formate

Config_Manager().create_config(config_as_json).encrypt()

```

thats it so far