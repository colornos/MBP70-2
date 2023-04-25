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
    temp_data = unpack('<BHxxxxxxI', bytes(values[0:14]))
    log.info(f'Temperature: {temp_data[0] / 100.0} C')

def main():
    config = ConfigParser()
    config.read('MBP70.ini')

    numeric_level = getattr(logging, config.get('Program', 'loglevel').upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    
    logging.basicConfig(level=numeric_level,
                        format='%(asctime)s %(levelname)-8s %(funcName)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=config.get('Program', 'logfile'),
                        filemode='w')
    log = logging.getLogger(__name__)

    ble_address = config.get('TEMP', 'ble_address')
    device_name = config.get('TEMP', 'device_name')
    device_model = config.get('TEMP', 'device_model')

    adapter = pygatt.backends.GATTToolBackend()
    adapter.start()

    while True:
        try:
            device = adapter.connect(ble_address)
            device.subscribe(Char_temperature, callback=handle_temperature_data, indication=True)
            time.sleep(30)  # Adjust the sleep time as needed
            device.disconnect()
        except pygatt.exceptions.NotConnectedError:
            log.error("Device not connected")
            time.sleep(5)  # Retry after a short delay

if __name__ == "__main__":
    main()
