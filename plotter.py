# importing the requests library
import requests, json
from requests.auth import HTTPBasicAuth
import matplotlib.pyplot as plt


class ReadApi:
    def __init__(self):
        self.URL = "https://analyzer-app-i524883.cfapps.sap.hana.ondemand.com/getMetrics"
        self.username = "lovish.mehta@sap.com"
        self.password = "123456"
    
    def requestData(self):
        request_object = requests.get(url = self.URL, auth = HTTPBasicAuth(self.username, self.password))
        # extracting data in json format
        if request_object == 200:
            data = request_object.json()
        else:
            raise Exception("Error code returned:{}", request_object)
        return data

class Plotter:
    def __init__(self):
        readApi = ReadApi()
        self.json_data = readApi.requestData()
        if not self.json_data:
            raise Exception("The data returned from API is empty. Cannot create plots")
        else:
            writeJson(self.json_data)
        
    def writeJson(self):
        # Serializing json 
        json_object = json.dumps(self.json_data, indent = 4)  
        # Writing to sample.json
        with open("requestObject.json", "w") as outfile:
            outfile.write(json_object)


