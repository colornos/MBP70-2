#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import logging
from configparser import ConfigParser
import os
import threading
import urllib3

http = urllib3.PoolManager()

class Plugin:

    def __init__(self):
        self.name = "MBP70plugintemplate2"

    def execute(self, config, temperature_data):

        def read_from_file(filename):
            with open(filename, "r") as file:
                contents = file.read()
            return contents

        rfid = read_from_file("rfid.txt")

        if (rfid == "0"):
            print("No card detected!")
        else:
            temperature = temperature_data[0]['temperature']
            r = http.request('POST', 'https://colornos.com/sensors/temperature.php', fields={"rfid": rfid, "one": temperature})
            print(r.data)
            log.info('Finished plugin: ' + __name__)
