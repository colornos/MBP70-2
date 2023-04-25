import sys
import pygatt.backends
import logging
from configparser import ConfigParser
import time
import subprocess
from struct import *
from binascii import hexlify
import os

# Interesting characteristics
Char_temperature = '00002A1C-0000-1000-8000-00805f9b34fb'  # temperature data

def handle_temperature_data(handle, value):
    temp_data = unpack('<HBBBBBB', value)
    temperature = temp_data[0] / 100.0
    log.info(f'Temperature: {temperature} C')
    print(f"Received temperature data: {temperature} C")

# Reading configuration file
config = ConfigParser()
config.read('MBP70.ini')

# Set up logging
log = logging.getLogger(__name__)
log.setLevel(config.get('Program', 'loglevel').upper())
fh = logging.FileHandler(config.get('Program', 'logfile'))
fh.setLevel(config.get('Program', 'loglevel').upper())
log.addHandler(fh)

# Discovering device
adapter = pygatt.backends.GATTToolBackend()
adapter.start()
log.info('Discovering device...')
device = None

while not device:
    try:
        device = adapter.connect(config.get('TEMP', 'ble_address'))
        log.info('Device connected')
    except Exception as e:
        log.error(f'Error connecting to device: {e}')
        time.sleep(5)

# Reading temperature data
while True:
    try:
        device.subscribe(Char_temperature, callback=handle_temperature_data)
        print("Subscribed to temperature data.")
    except Exception as e:
        log.error(f'Error reading temperature data: {e}')
        device.disconnect()
        time.sleep(5)
        while not device:
            try:
                device = adapter.connect(config.get('TEMP', 'ble_address'))
                log.info('Device reconnected')
            except Exception as e:
                log.error(f'Error reconnecting to device: {e}')
                time.sleep(5)

# Disconnect and stop the adapter
device.disconnect()
adapter.stop()
