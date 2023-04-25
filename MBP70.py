import sys
import pygatt.backends
import logging
from configparser import ConfigParser
import time
import subprocess
from struct import *
from binascii import hexlify
import os
import glob
import importlib
from datetime import datetime

# Interesting characteristics
Char_temperature = '00002A1C-0000-1000-8000-00805f9b34fb'  # temperature data

def handle_temperature_data(handle, value):
    temp_data = unpack('<HBBBBBB', value)
    log.info(f'Temperature: {temp_data[0] / 100.0} C')

# Read configuration
config = configparser.ConfigParser()
config.read("config.ini")

# Get temperature data (dummy data for this example)
temperature_data = [{"temperature": 25.5}]

# Dynamically load plugins
plugin_folder = "plugins"
plugin_files = glob.glob(os.path.join(plugin_folder, "*.py"))

loaded_plugins = []

for plugin_file in plugin_files:
    plugin_name = os.path.basename(plugin_file)[:-3]
    spec = importlib.util.spec_from_file_location(plugin_name, plugin_file)
    plugin_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plugin_module)
    plugin = plugin_module.Plugin()
    loaded_plugins.append(plugin)
    print(f"Loaded plugin: {plugin.name}, {plugin}")

# Execute each plugin in a continuous loop
while True:
    for plugin in loaded_plugins:
        print(f"<module> Calling execute on plugin: {plugin.name}")
        plugin.execute(config, temperature_data)
    
    # Delay between iterations (in seconds)
    time.sleep(10)
