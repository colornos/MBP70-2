import http.client as http_client

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
            temperature = temperature_data[0]["temperature"]
            http_client.HTTPSConnection._http_vsn_str = "HTTP/1.0"
            conn = http_client.HTTPSConnection("colornos.com")
            headers = {"Content-type": "application/x-www-form-urlencoded"}

            data = f"rfid={rfid}&one={temperature}"
            conn.request("POST", "/sensors/temperature.php", data, headers)
            response = conn.getresponse()
            print(response.status, response.reason)
            print(response.read().decode())
            conn.close()
